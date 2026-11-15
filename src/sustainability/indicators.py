"""The dashboard calculations of design section 12 (Table 12.1). The database computes every figure;
nothing here comes from the AI."""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from django.db.models import Count, Q, Sum

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
    status: str = "Synthetic demo data"
    raw: dict = field(default_factory=dict)


def money(value):
    return f"AED {value:,.0f}"


def count(number, word):
    return f"{number} {word}{'' if number == 1 else 's'}"


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
        kg = f", {t['waste_diverted_kg']:.1f} kg" if t["waste_diverted_kg"] is not None else ""
        carbon = ("N/A" if t["co2e_low_kg"] is None else
                  f"About {t['co2e_low_kg']:,.0f} to {t['co2e_high_kg']:,.0f} kg CO2e saved (estimated)")
        rate = "N/A (nothing listed in this period)" if t["reuse_rate_percent"] is None else f"{t['reuse_rate_percent']}%"
        return [
            Indicator("waste", "Waste diverted", f"{count(t['items_reused'], 'item')}{kg}",
                      "Sum of quantities received through reuse. Mass = items x category mass per item.",
                      f"{count(t['completed_transfers'], 'completed transfer')}; {t['items_without_mass']} without a recorded mass",
                      "Completed transfers (TR-06). Monitor mass 5.15 kg from the Dell P2422H specifications (F3)."),
            Indicator("avoided", "Avoided purchases",
                      f"{count(t['avoided_purchase_requests'], 'request')}, {money(t['avoided_purchase_aed'])}",
                      "Count of fulfilled requests the receiving representative confirmed (BR-18). Value = quantity x replacement cost.",
                      "Only confirmed transfers count; 'no suitable item' never counts; "
                      f"{count(t['requests_without_price'], 'request')} without a cited replacement cost (N/A)",
                      "Replacement cost per category, e.g. monitor AED 345 incl. VAT, Phase 2 feasibility study [S15] (F7)."),
            Indicator("net", "Net financial savings", money(t["net_savings_aed"]),
                      "Avoided purchase value - transfer costs of the same transfers (no double counting).",
                      f"{money(t['avoided_purchase_aed'])} - {money(t['transfer_cost_aed'])}",
                      "Transfer costs entered on each transfer."),
            Indicator("carbon", "Carbon saved", carbon,
                      "For confirmed avoided purchases: sum of (quantity x category factor) - transport, shown as a "
                      "low-to-high range.",
                      f"Transport {t['transport_co2e_kg']:.2f} kg CO2e (van trips x km x {VAN_KG_CO2E_PER_KM}); "
                      f"{count(t['transfers_without_factor'], 'transfer')} in categories without a factor (N/A)",
                      "Monitor: UK DESNZ 2024 IT materials x 5.15 kg (F1, F3) to Dell P2422H PCF 327 kg (F2). "
                      f"Chair: FIRA average 27 kg (F4) to Steelcase Leap EPD 104 kg (F5). Van: {VAN_FACTOR_SOURCE} (F6)."),
            Indicator("reuse_rate", "Reuse rate", rate,
                      "Units listed in the period and received by its end / units listed in the period x 100.",
                      f"{t['cohort_units_reused']} of {t['cohort_units']} listed units",
                      "Listings and completed transfers in the period."),
        ]
