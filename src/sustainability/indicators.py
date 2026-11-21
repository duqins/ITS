"""The dashboard calculations of design section 12 (Table 12.1). The database computes every figure;
nothing here comes from the AI."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Count, Q, Sum
from django.utils.translation import gettext as _, gettext_lazy, ngettext

from transfers.models import Transfer

from .models import VAN_FACTOR_SOURCE, VAN_KG_CO2E_PER_KM, SustainabilityImpact


@dataclass
class Indicator:
    key: str
    name: str
    value: str
    formula: str
    inputs: str
    source: str
    status: str = gettext_lazy("Synthetic demo data")
    raw: dict = field(default_factory=dict)
    tone: str = ""  # "good" (green) or "bad" (red) where the direction is clear, as for net savings


def money(value):
    return _("AED %(amount)s") % {"amount": f"{value:,.0f}"}


class SustainabilityIndicators:
    """Works out the indicators for one period and (optionally) one department."""

    def __init__(self, date_from: date, date_to: date, department=None):
        self.date_from, self.date_to, self.department = date_from, date_to, department
        impacts = SustainabilityImpact.objects.filter(occurred_on__gte=date_from, occurred_on__lte=date_to)
        if department is not None:
            impacts = impacts.filter(department=department)
        self.impacts = impacts.select_related("transfer__asset__category", "department")

    def totals(self):
        """The plain numbers, also given to the AI report draft so it cannot invent figures."""
        agg = self.impacts.aggregate(
            transfers=Count("id"), items=Sum("items_diverted"), kg=Sum("waste_diverted_kg"),
            no_mass=Count("id", filter=Q(waste_diverted_kg__isnull=True)),
        )
        # Money and carbon come from avoided purchases the receiving representative confirmed (BR-18, Table 12.1).
        # A category without a cited replacement cost has no avoided value (N/A), so its transfer cost is left
        # out of the net savings too; otherwise reusing it would look like a loss.
        priced = Q(avoided_purchase_aed__isnull=False)
        confirmed = self.impacts.filter(purchase_avoided_confirmed=True).aggregate(
            requests=Count("id"), avoided=Sum("avoided_purchase_aed"), cost=Sum("transfer_cost_aed", filter=priced),
            no_price=Count("id", filter=~priced),
            low=Sum("co2e_low_kg"), high=Sum("co2e_high_kg"), transport=Sum("transport_co2e_kg"),
            no_factor=Count("id", filter=Q(co2e_low_kg__isnull=True)))
        avoided = confirmed["avoided"] or Decimal("0")
        cost = confirmed["cost"] or Decimal("0")
        return {
            "completed_transfers": agg["transfers"],
            "items_reused": agg["items"] or 0,
            "waste_diverted_kg": agg["kg"],
            "items_without_mass": agg["no_mass"],
            "avoided_purchase_requests": confirmed["requests"],
            "avoided_purchase_aed": avoided,
            "transfer_cost_aed": cost,
            "requests_without_price": confirmed["no_price"],
            "net_savings_aed": avoided - cost,
            "co2e_low_kg": confirmed["low"],
            "co2e_high_kg": confirmed["high"],
            "transport_co2e_kg": confirmed["transport"] or Decimal("0"),
            "transfers_without_factor": confirmed["no_factor"],
            **self.reuse_rate(),
        }

    def savings_by_month(self):
        """The dashboard graph: net savings added up month by month over the period, with the same rules as
        totals() (confirmed avoided purchases with a cited price, minus the costs of those same transfers), so
        the last month always equals the net savings card."""
        added = {}
        for day, avoided, cost in self.impacts.filter(
                purchase_avoided_confirmed=True, avoided_purchase_aed__isnull=False).values_list(
                "occurred_on", "avoided_purchase_aed", "transfer_cost_aed"):
            month = day.replace(day=1)
            added[month] = added.get(month, Decimal("0")) + avoided - cost
        months, running, month = [], Decimal("0"), self.date_from.replace(day=1)
        while month <= self.date_to:
            running += added.get(month, Decimal("0"))
            months.append((month, running))
            month = (month.replace(day=28) + timedelta(days=4)).replace(day=1)
        return months

    def reuse_rate(self):
        """Units listed in the period (the cohort) that were transferred and received by its end (SU-05)."""
        from assets.models import Listing

        cohort = Listing.objects.filter(published_at__date__gte=self.date_from, published_at__date__lte=self.date_to)
        if self.department is not None:
            cohort = cohort.filter(asset__owner_department=self.department)
        listed = cohort.aggregate(total=Sum("quantity"))["total"] or 0
        received = Transfer.objects.filter(
            reservation__listing__in=cohort, status=Transfer.Status.COMPLETED, received_at__date__lte=self.date_to,
        ).aggregate(total=Sum("received_quantity"))["total"] or 0
        return {"cohort_units": listed, "cohort_units_reused": received,
                "reuse_rate_percent": round(received * 100 / listed, 1) if listed else None}

    def indicators(self):
        t = self.totals()
        items, transfers, requests = t["items_reused"], t["completed_transfers"], t["avoided_purchase_requests"]
        no_price, no_factor, listed = t["requests_without_price"], t["transfers_without_factor"], t["cohort_units"]
        if t["waste_diverted_kg"] is None:
            waste = ngettext("%(count)s item", "%(count)s items", items) % {"count": items}
        else:
            waste = ngettext("%(count)s item, %(kg)s kg", "%(count)s items, %(kg)s kg", items) % {
                "count": items, "kg": f"{t['waste_diverted_kg']:.1f}"}
        carbon = (_("N/A") if t["co2e_low_kg"] is None else
                  _("About %(low)s to %(high)s kg CO2e saved (estimated)") % {
                      "low": f"{t['co2e_low_kg']:,.0f}", "high": f"{t['co2e_high_kg']:,.0f}"})
        rate = (_("N/A (nothing listed in this period)") if t["reuse_rate_percent"] is None
                else f"{t['reuse_rate_percent']}%")
        return [
            Indicator("waste", _("Waste diverted"), waste,
                      _("Sum of quantities received through reuse. Mass = items x category mass per item."),
                      ngettext("%(count)s completed transfer; %(without)s without a recorded mass",
                               "%(count)s completed transfers; %(without)s without a recorded mass", transfers) % {
                          "count": transfers, "without": t["items_without_mass"]},
                      _("Completed transfers (TR-06). Monitor mass 5.15 kg from the Dell P2422H specifications (F3).")),
            Indicator("avoided", _("Avoided purchases"),
                      ngettext("%(count)s request, %(value)s", "%(count)s requests, %(value)s", requests) % {
                          "count": requests, "value": money(t["avoided_purchase_aed"])},
                      _("Count of fulfilled requests the receiving representative confirmed (BR-18). "
                        "Value = quantity x replacement cost."),
                      ngettext("Only confirmed transfers count; 'no suitable item' never counts; "
                               "%(count)s request without a cited replacement cost (N/A)",
                               "Only confirmed transfers count; 'no suitable item' never counts; "
                               "%(count)s requests without a cited replacement cost (N/A)", no_price) % {
                          "count": no_price},
                      _("Replacement cost per category, e.g. monitor AED 345 incl. VAT, "
                        "Phase 2 feasibility study [S15] (F7).")),
            Indicator("net", _("Net financial savings"), money(t["net_savings_aed"]),
                      _("Avoided purchase value - transfer costs of the same transfers (no double counting)."),
                      f"{money(t['avoided_purchase_aed'])} - {money(t['transfer_cost_aed'])}",
                      _("Transfer costs entered on each transfer."),
                      tone="good" if t["net_savings_aed"] > 0 else "bad" if t["net_savings_aed"] < 0 else ""),
            Indicator("carbon", _("Carbon saved"), carbon,
                      _("For confirmed avoided purchases: sum of (quantity x category factor) - transport, shown as a "
                        "low-to-high range."),
                      ngettext("Transport %(transport)s kg CO2e (van trips x km x %(factor)s); "
                               "%(count)s transfer in categories without a factor (N/A)",
                               "Transport %(transport)s kg CO2e (van trips x km x %(factor)s); "
                               "%(count)s transfers in categories without a factor (N/A)", no_factor) % {
                          "transport": f"{t['transport_co2e_kg']:.2f}", "factor": VAN_KG_CO2E_PER_KM,
                          "count": no_factor},
                      _("Monitor: UK DESNZ 2024 IT materials x 5.15 kg (F1, F3) to Dell P2422H PCF 327 kg (F2). "
                        "Chair: FIRA average 27 kg (F4) to Steelcase Leap EPD 104 kg (F5). Van: %(van)s (F6).") % {
                          "van": VAN_FACTOR_SOURCE}),
            Indicator("reuse_rate", _("Reuse rate"), rate,
                      _("Units listed in the period and received by its end / units listed in the period x 100."),
                      # Same English for one and many; the plural form lets Arabic agree with the number.
                      ngettext("%(reused)s of %(listed)s listed units", "%(reused)s of %(listed)s listed units",
                               listed) % {"reused": t["cohort_units_reused"], "listed": listed},
                      _("Listings and completed transfers in the period.")),
        ]
