"""The demo history (months of finished transfers, more items, overdue work) and the savings graph on the
dashboard, added after the TA review on 17 November."""

import re
from datetime import date
from decimal import Decimal

from django.utils import timezone

from ai.matching import EligibilityChecker
from assets.models import Asset, Listing
from resource_requests.models import ResourceRequest
from sustainability.charts import savings_chart
from sustainability.indicators import SustainabilityIndicators
from sustainability.models import SustainabilityImpact
from transfers.models import Approval, Transfer

from .helpers import DemoTestCase


def card_number(html, label):
    """The number on a home page card, found by its label."""
    match = re.search(r'data-count="(\d+)">\d+</div><div class="label">' + re.escape(label) + "<", html)
    return int(match.group(1)) if match else None


class HistoryTests(DemoTestCase):
    with_history = True

    def test_the_history_spans_months_and_money_only_comes_from_priced_monitors(self):
        self.assertEqual(Transfer.objects.filter(status=Transfer.Status.COMPLETED).count(), 10)
        months = {d.replace(day=1) for d in SustainabilityImpact.objects.values_list("occurred_on", flat=True)}
        self.assertGreaterEqual(len(months), 5)
        priced = SustainabilityImpact.objects.filter(avoided_purchase_aed__isnull=False)
        # Only the monitor category has a cited replacement price; chairs and desks stay N/A (no guessing).
        self.assertEqual(set(priced.values_list("transfer__asset__category__subcategory", flat=True)), {"Monitor"})
        # Every step of a finished transfer happened in order, on its own day.
        for transfer in Transfer.objects.filter(status=Transfer.Status.COMPLETED):
            self.assertLessEqual(transfer.created_at, transfer.handed_over_at)
            self.assertLessEqual(transfer.handed_over_at, transfer.received_at)
            self.assertLessEqual(transfer.received_at, timezone.now())

    def test_the_section_12_worked_example_is_still_there(self):
        example = Transfer.objects.order_by("pk").first()
        self.assertEqual(example.quantity, 2)
        self.assertEqual(example.impact.avoided_purchase_aed, Decimal("690.00"))
        self.assertEqual(example.impact.avoided_purchase_aed - example.impact.transfer_cost_aed, Decimal("650.00"))

    def test_the_demo_path_is_unchanged(self):
        chairs = ResourceRequest.objects.get(purpose__startswith="Chairs")
        self.assertEqual([l.asset.name for l in EligibilityChecker().eligible(chairs)], ["Ergonomic office chair"])
        projector = ResourceRequest.objects.get(purpose__startswith="Projector")
        self.assertEqual([l.asset.name for l in EligibilityChecker().eligible(projector)], ["Epson classroom projector"])
        computing = Asset.objects.filter(owner_department__code="COMP").filter(Asset.needing_verification())
        self.assertEqual(list(computing.values_list("name", flat=True)), ["Standing desk"])

    def test_there_is_more_to_search_and_some_work_is_overdue(self):
        self.assertGreaterEqual(Listing.objects.filter(status=Listing.Status.PUBLISHED).count(), 10)
        overdue = [a for a in Approval.objects.filter(status=Approval.Status.PENDING) if a.is_overdue()]
        self.assertEqual(sorted(a.stage for a in overdue),
                         sorted([Approval.Stage.REQUEST_DEPARTMENT, Approval.Stage.TRANSFER_FINANCE]))
        self.assertEqual(card_number(self.sign_in("comp.rep").get("/").content.decode(), "Overdue tasks"), 1)
        self.assertEqual(card_number(self.sign_in("finance.officer").get("/").content.decode(), "Overdue tasks"), 1)

    def test_the_graph_ends_at_the_net_savings_card(self):
        today = timezone.localdate()
        scope = SustainabilityIndicators(date(today.year, 1, 1), today)
        months = scope.savings_by_month()
        self.assertEqual(months[-1][1], scope.totals()["net_savings_aed"])
        self.assertEqual(months[0][0], date(today.year, 1, 1))
        self.assertEqual([m for m, _ in months], sorted(m for m, _ in months))
        page = self.sign_in("sustainability.officer").get("/sustainability/").content.decode()
        self.assertIn('class="savings-chart is-good"', page)
        self.assertIn("tone-good", page)
        self.assertIn("Saving money", page)
        net = f"{scope.totals()['net_savings_aed']:,.0f}"
        self.assertIn(f"AED {net}", page)

    def test_the_graph_follows_the_department_filter_and_the_representative_scope(self):
        today = timezone.localdate()
        engineering = SustainabilityIndicators(date(today.year, 1, 1), today,
                                               department=Asset.objects.get(name__startswith="Epson").owner_department)
        self.assertTrue(all(total == 0 for _, total in engineering.savings_by_month()))
        # Omar, the Computing representative, sees only Computing; every finished transfer went to Computing.
        page = self.sign_in("comp.rep").get("/sustainability/").content.decode()
        self.assertIn("savings-chart", page)


class ChartTests(DemoTestCase):
    def test_a_loss_is_drawn_in_red_below_the_zero_line(self):
        months = [(date(2026, 1, 1), Decimal("100")), (date(2026, 2, 1), Decimal("-250"))]
        chart = savings_chart(months)
        self.assertFalse(chart["good"])
        self.assertIn(0, [t["value"] for t in chart["ticks"]])
        self.assertGreater(chart["points"][1]["y"], chart["zero"])  # below zero is lower on the screen
        self.assertIsNone(savings_chart([]))

    def test_without_history_the_dashboard_still_works(self):
        page = self.sign_in("sustainability.officer").get("/sustainability/").content.decode()
        self.assertIn("savings-chart", page)
        self.assertIn("AED 650", page)
