"""Validation of the sustainability calculations (design section 12, SU-01 to SU-08).

Ten cases. In each one the expected value is worked out by hand from the formulas of Table 12.1 and the
factors of Table 12.2, written as a comment, and then compared with what the app calculates.
"""

from datetime import date, timedelta
from decimal import Decimal

from django.utils import timezone

from accounts.models import User
from assets.models import Condition, Listing
from audit.lifecycle import BusinessRuleError
from resource_requests.models import ResourceRequest
from sustainability.indicators import SustainabilityIndicators
from sustainability.models import SustainabilityImpact
from transfers.models import Reservation, Transfer

from .helpers import DemoTestCase

# The factors of Table 12.2 and the ranges of Table 12.3.
MONITOR_MASS_KG = Decimal("5.15")      # F3
MONITOR_PRICE_AED = Decimal("345")     # F7
MONITOR_LOW = Decimal("128.057")       # F1 x F3 = 24.86548 x 5.15
MONITOR_HIGH = Decimal("327")          # F2
CHAIR_LOW, CHAIR_HIGH = Decimal("27"), Decimal("104")   # F4, F5
VAN_PER_KM = Decimal("0.25561")        # F6


class ValidationCase(DemoTestCase):
    """Helpers that move an item from Engineering to Computing through the real workflow."""

    def setUp(self):
        self.users = {u.username: u for u in User.objects.all()}
        self.today = timezone.localdate()

    def totals(self, days_back=30, department=None):
        return SustainabilityIndicators(self.today - timedelta(days=days_back), self.today, department).totals()

    def move(self, item, quantity, request=None, **details):
        """Request, hold, transfer, both approvals, handover and receipt. Returns the impact of the transfer."""
        listing = Listing.objects.get(asset__name__startswith=item)
        if request is None:
            requester = self.users["comp.requester"]
            request = ResourceRequest.objects.create(
                purpose=f"{quantity} x {item}", category=listing.asset.category, quantity=quantity,
                min_condition=Condition.POOR, required_by=self.today + timedelta(days=20), requester=requester,
                department=requester.department)
            request.submit(requester)
            request.approve(self.users["comp.rep"])
        hold = Reservation.request_hold(request, listing, request.requester)
        hold.confirm(self.users["eng.custodian"])
        transfer = Transfer.start(hold, request.requester, self.users["comp.custodian"], **details)
        transfer.approve_stage(self.users["eng.rep"])
        transfer.approve_stage(self.users["comp.rep"])
        transfer.hand_over(self.users["eng.custodian"], listing.asset.condition)
        transfer.confirm_receipt(self.users["comp.custodian"], quantity, listing.asset.condition)
        return SustainabilityImpact.objects.get(transfer=transfer)

    def set_example_aside(self):
        """Date the seed's worked example 40 days back, so a 30-day period holds only the new transfer."""
        example = SustainabilityImpact.objects.order_by("pk").first()   # the seed's transfer is the first impact
        SustainabilityImpact.objects.filter(pk=example.pk).update(occurred_on=self.today - timedelta(days=40))


class SustainabilityValidationTests(ValidationCase):
    def test_case_01_worked_example_of_section_12(self):
        # 2 monitors, one van trip of 10 km, transfer cost AED 40 (Table 12.4).
        impact, totals = SustainabilityImpact.objects.get(), self.totals()
        self.assertEqual(impact.waste_diverted_kg, Decimal("10.30"))       # 2 x 5.15 = 10.30
        self.assertEqual(impact.avoided_purchase_aed, Decimal("690.00"))   # 2 x 345 = 690
        self.assertEqual(totals["net_savings_aed"], Decimal("650.00"))     # 690 - 40 = 650
        self.assertEqual(impact.transport_co2e_kg, Decimal("2.56"))        # 1 x 10 x 0.25561 = 2.5561
        self.assertEqual(impact.co2e_low_kg, Decimal("253.55"))            # 2 x 128.057 - 2.56 = 253.554
        self.assertEqual(impact.co2e_high_kg, Decimal("651.44"))           # 2 x 327 - 2.56 = 651.44
        # The document gives the range to one decimal: 253.6 to 651.4.
        self.assertEqual((round(totals["co2e_low_kg"], 1), round(totals["co2e_high_kg"], 1)),
                         (Decimal("253.6"), Decimal("651.4")))
        self.assertEqual(impact.factor_version, "Section 12 v1")           # SU-08: the factor version is kept

    def test_case_03_chairs_have_a_carbon_range_but_no_money_value(self):
        # 2 office chairs, one van trip of 4 km, transfer cost AED 25. Chairs have no cited price or mass.
        impact = self.move("Ergonomic", 2, van_trips=1, distance_km=Decimal("4"), transfer_cost_aed=Decimal("25"))
        self.assertEqual(impact.transport_co2e_kg, Decimal("1.02"))        # 1 x 4 x 0.25561 = 1.02244
        self.assertEqual(impact.co2e_low_kg, Decimal("52.98"))             # 2 x 27 - 1.02 = 52.98
        self.assertEqual(impact.co2e_high_kg, Decimal("206.98"))           # 2 x 104 - 1.02 = 206.98
        self.assertIsNone(impact.avoided_purchase_aed)                     # N/A, not 0 and not guessed
        self.assertIsNone(impact.waste_diverted_kg)                        # no recorded mass: N/A
        impact.confirm_avoided_purchase(self.users["comp.rep"])
        totals = self.totals()
        self.assertEqual(totals["requests_without_price"], 1)
        self.assertEqual(totals["avoided_purchase_aed"], Decimal("690.00"))   # still only the 2 monitors
        self.assertEqual(totals["co2e_low_kg"], Decimal("306.53"))         # 253.55 + 52.98
        self.assertEqual(totals["co2e_high_kg"], Decimal("858.42"))        # 651.44 + 206.98

    def test_case_04_a_category_without_a_factor_shows_na(self):
        # The projector's category has no carbon factor, no mass and no cited price (Table 12.3: N/A).
        impact = self.move("Epson", 1, request=ResourceRequest.objects.get(purpose__startswith="Projector"))
        impact.confirm_avoided_purchase(self.users["comp.rep"])
        self.assertEqual(impact.items_diverted, 1)
        self.assertIsNone(impact.co2e_low_kg)
        self.assertIsNone(impact.co2e_high_kg)
        self.set_example_aside()
        totals = self.totals()                                             # only the projector is in the period
        self.assertEqual(totals["items_reused"], 1)                        # the item still counts as reused
        self.assertIsNone(totals["co2e_low_kg"])                           # N/A, not 0
        self.assertEqual(totals["transfers_without_factor"], 1)
        carbon = next(i for i in SustainabilityIndicators(self.today - timedelta(days=30), self.today).indicators()
                      if i.key == "carbon")
        self.assertEqual(carbon.value, "N/A")

    def test_case_05_an_avoided_purchase_counts_only_after_it_is_confirmed(self):
        # 1 more monitor, one van trip of 3 km, transfer cost AED 20.
        impact = self.move("Dell", 1, van_trips=1, distance_km=Decimal("3"), transfer_cost_aed=Decimal("20"))
        before = self.totals()
        self.assertEqual(before["items_reused"], 3)                        # 2 + 1: reuse itself counts at receipt
        self.assertEqual(before["waste_diverted_kg"], Decimal("15.45"))    # 3 x 5.15 = 15.45
        self.assertEqual(before["avoided_purchase_aed"], Decimal("690.00"))   # not confirmed yet (BR-18)
        self.assertEqual(before["net_savings_aed"], Decimal("650.00"))
        self.assertEqual(before["co2e_low_kg"], Decimal("253.55"))
        impact.confirm_avoided_purchase(self.users["comp.rep"])
        after = self.totals()
        self.assertEqual(after["avoided_purchase_requests"], 2)
        self.assertEqual(after["avoided_purchase_aed"], Decimal("1035.00"))   # 690 + 1 x 345 = 1,035
        self.assertEqual(after["net_savings_aed"], Decimal("975.00"))      # 1,035 - (40 + 20) = 975
        self.assertEqual(after["co2e_low_kg"], Decimal("380.84"))          # 253.55 + (128.057 - 0.77) = 380.84
        self.assertEqual(after["co2e_high_kg"], Decimal("977.67"))         # 651.44 + (327 - 0.77) = 977.67

    def test_case_06_the_same_avoided_purchase_is_never_counted_twice(self):
        impact = self.move("Dell", 1, van_trips=1, distance_km=Decimal("3"), transfer_cost_aed=Decimal("20"))
        impact.confirm_avoided_purchase(self.users["comp.rep"])
        once = self.totals()
        with self.assertRaisesMessage(BusinessRuleError, "already confirmed"):
            impact.confirm_avoided_purchase(self.users["comp.rep"])
        self.assertEqual(self.totals(), once)                              # every figure is unchanged
        self.assertEqual(SustainabilityImpact.objects.filter(transfer=impact.transfer).count(), 1)

    def test_case_07_a_reuse_rate_with_nothing_listed_is_na(self):
        # Computing has listed nothing, and nothing was listed in 2020: the denominator is 0.
        computing = self.users["comp.rep"].department
        self.assertIsNone(self.totals(department=computing)["reuse_rate_percent"])
        old = SustainabilityIndicators(date(2020, 1, 1), date(2020, 12, 31))
        self.assertEqual(old.reuse_rate(), {"cohort_units": 0, "cohort_units_reused": 0, "reuse_rate_percent": None})
        rate = next(i for i in old.indicators() if i.key == "reuse_rate")
        self.assertEqual(rate.value, "N/A (nothing listed in this period)")

    def test_case_08_reuse_rate_by_hand(self):
        # Listed: 4 monitors + 6 chairs + 1 projector + 1 oscilloscope = 12 units. Received: 2 monitors.
        rate = SustainabilityIndicators(self.today - timedelta(days=30), self.today).reuse_rate()
        self.assertEqual((rate["cohort_units"], rate["cohort_units_reused"]), (12, 2))
        self.assertEqual(rate["reuse_rate_percent"], 16.7)                 # 2 / 12 x 100 = 16.67
        self.move("Dell", 1)
        self.assertEqual(self.totals()["reuse_rate_percent"], 25.0)        # 3 / 12 x 100 = 25.0

    def test_case_09_a_loss_stays_negative(self):
        # 1 monitor moved at a cost of AED 500, more than the AED 345 it saves.
        impact = self.move("Dell", 1, van_trips=1, distance_km=Decimal("3"), transfer_cost_aed=Decimal("500"))
        impact.confirm_avoided_purchase(self.users["comp.rep"])
        self.set_example_aside()
        totals = self.totals()                                             # only this transfer is in the period
        self.assertEqual(totals["avoided_purchase_aed"], Decimal("345.00"))
        self.assertEqual(totals["net_savings_aed"], Decimal("-155.00"))    # 345 - 500 = -155
        net = next(i for i in SustainabilityIndicators(self.today - timedelta(days=30), self.today).indicators()
                   if i.key == "net")
        self.assertEqual((net.value, net.tone), ("AED -155", "bad"))

    def test_case_10_a_transfer_outside_the_period_is_not_counted(self):
        # The worked example was received today. A period that ends yesterday must not contain it.
        earlier = SustainabilityIndicators(self.today - timedelta(days=30), self.today - timedelta(days=1)).totals()
        self.assertEqual((earlier["completed_transfers"], earlier["items_reused"]), (0, 0))
        self.assertEqual((earlier["avoided_purchase_aed"], earlier["net_savings_aed"]), (Decimal("0"), Decimal("0")))
        self.assertIsNone(earlier["waste_diverted_kg"])                    # nothing to add up: N/A
        self.assertIsNone(earlier["co2e_low_kg"])
        self.assertIsNone(earlier["reuse_rate_percent"])                   # nothing was listed before today
        self.assertEqual(self.totals()["completed_transfers"], 1)          # the period up to today contains it


class HistoryValidationTests(ValidationCase):
    with_history = True

    def test_case_02_net_savings_of_the_whole_demo_history(self):
        # Seven monitor transfers were confirmed: 2 + 3 + 1 + 4 + 2 + 2 + 1 = 15 monitors.
        # Avoided purchases: 15 x 345 = 5,175. Their costs: 40 + 30 + 15 + 50 + 40 + 40 + 20 = 235.
        # Net savings: 5,175 - 235 = 4,940. Two chair transfers and one desk transfer have no cited price.
        monitors = Transfer.objects.filter(status=Transfer.Status.COMPLETED, asset__category__subcategory="Monitor")
        avoided = sum(t.received_quantity * MONITOR_PRICE_AED for t in monitors)
        costs = sum(t.transfer_cost_aed for t in monitors)
        self.assertEqual((monitors.count(), avoided, costs), (7, Decimal("5175"), Decimal("235")))
        totals = self.totals(days_back=400)
        self.assertEqual(totals["avoided_purchase_aed"], avoided)
        self.assertEqual(totals["transfer_cost_aed"], costs)
        self.assertEqual(totals["net_savings_aed"], Decimal("4940.00"))
        self.assertEqual(totals["requests_without_price"], 3)              # 2 chair transfers and 1 desk transfer
        self.assertEqual(totals["items_reused"], 21)                       # 15 monitors + 2 + 3 chairs + 1 desk
        self.assertEqual(totals["waste_diverted_kg"], Decimal("77.25"))    # 15 x 5.15 = 77.25 (monitors only)
        scope = SustainabilityIndicators(self.today - timedelta(days=400), self.today)
        self.assertEqual(scope.savings_by_month()[-1][1], Decimal("4940.00"))   # the graph ends at the same figure
