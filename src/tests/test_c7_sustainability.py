"""C7 Sustainability dashboard: the seed's completed transfer is the worked example of design section 12."""

from datetime import date
from decimal import Decimal

from sustainability.indicators import SustainabilityIndicators

from .helpers import DemoTestCase


class SustainabilityTests(DemoTestCase):
    def test_worked_example_figures(self):
        totals = SustainabilityIndicators(date(date.today().year, 1, 1), date.today()).totals()
        self.assertEqual(totals["items_reused"], 2)
        self.assertEqual(totals["waste_diverted_kg"], Decimal("10.30"))
        self.assertEqual(totals["avoided_purchase_aed"], Decimal("690.00"))
        self.assertEqual(totals["net_savings_aed"], Decimal("650.00"))
        self.assertEqual(totals["transport_co2e_kg"], Decimal("2.56"))
        self.assertEqual(round(totals["co2e_low_kg"], 1), Decimal("253.6"))
        self.assertEqual(round(totals["co2e_high_kg"], 1), Decimal("651.4"))

    def test_dashboard_shows_measures_with_formula_and_source(self):
        response = self.sign_in("sustainability.officer").get("/sustainability/")
        for text in ("Waste diverted", "Avoided purchases", "Net financial savings", "Carbon saved", "Reuse rate",
                     "AED 690", "F7", "0.25561"):
            self.assertContains(response, text)

    def test_reversed_dates_are_refused(self):
        response = self.sign_in("sustainability.officer").get("/sustainability/?date_from=2026-12-01&date_to=2026-01-01")
        self.assertContains(response, "on or before the end date")

    def test_requester_cannot_open_the_dashboard(self):
        self.assertEqual(self.sign_in("comp.requester").get("/sustainability/").status_code, 403)
