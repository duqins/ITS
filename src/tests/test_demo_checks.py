"""Problems found in the full check before the demo, each with the test that keeps it fixed."""

from django.utils import timezone

from assets.forms import ListingForm
from assets.models import Asset, Category, Condition, FurnitureAsset, ITAsset, Listing
from audit.lifecycle import BusinessRuleError
from audit.models import AuditLog
from resource_requests.models import ResourceRequest
from sustainability.indicators import SustainabilityIndicators
from sustainability.models import SustainabilityImpact
from transfers.models import Reservation

from . import test_edge_cases
from .helpers import DemoTestCase


class DemoCheckTests(DemoTestCase):
    # Reuse the edge-case helpers only. Naming that test class here would make the runner run its tests twice.
    setUp = test_edge_cases.EdgeCaseTests.setUp
    new_request = test_edge_cases.EdgeCaseTests.new_request
    transfer_for = test_edge_cases.EdgeCaseTests.transfer_for

    def complete(self, transfer, quantity, condition=Condition.FAIR):
        transfer.approve_stage(self.users["eng.rep"])
        transfer.approve_stage(self.users["comp.rep"])
        transfer.hand_over(self.users["eng.custodian"], condition)
        transfer.confirm_receipt(self.users["comp.custodian"], quantity, condition)
        transfer.refresh_from_db()
        return transfer

    def test_editing_an_it_draft_keeps_the_new_values(self):
        custodian = self.sign_in("eng.custodian")
        custodian.post("/assets/register/", {"kind": "it", "name": "HP laptop", "condition": "good", "quantity": 1,
                                             "campus": "Main campus", "serial_number": "SN-9"})
        asset = Asset.objects.get(name="HP laptop")
        laptop = Category.objects.get(subcategory="Laptop")
        custodian.post(f"/assets/{asset.pk}/edit/", {"name": "HP laptop 14", "category": laptop.pk, "condition": "fair",
                                                     "quantity": 2, "campus": "Main campus", "serial_number": "SN-10"})
        asset.refresh_from_db()
        self.assertEqual((asset.name, asset.category, asset.condition, asset.quantity), ("HP laptop 14", laptop, "fair", 2))
        self.assertEqual(ITAsset.objects.get(pk=asset.pk).serial_number, "SN-10")

    def test_export_csv_works_without_pressing_apply(self):
        response = self.sign_in("business.admin").get("/reports/?format=csv")
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_a_department_cannot_transfer_to_itself(self):
        desk = Asset.objects.get(name="Standing desk")
        listing = Listing.objects.create(asset=desk, quantity=1, created_by=self.users["comp.custodian"],
                                         status=Listing.Status.PUBLISHED, published_at=timezone.now())
        request = self.new_request("A desk", desk.category)
        with self.assertRaisesMessage(BusinessRuleError, "already belongs to your department"):
            Reservation.request_hold(request, listing, request.requester)
        from ai.matching import EligibilityChecker
        self.assertNotIn(listing, EligibilityChecker().eligible(request))

    def test_one_open_listing_per_asset(self):
        chairs = Asset.objects.get(name__startswith="Ergonomic")
        form = ListingForm({"quantity": 1, "available_from": timezone.localdate(), "release_reason": "surplus"},
                           asset=chairs)
        self.assertFalse(form.is_valid())
        self.assertIn("already offered", str(form.errors))

    def test_listing_stays_open_while_another_hold_is_running(self):
        listing = Listing.objects.get(asset__name__startswith="Ergonomic")
        category = listing.asset.category
        four = self.new_request("Four chairs", category, quantity=4)
        two = self.new_request("Two chairs", category, quantity=2, requester="comp.rep")
        transfer = self.transfer_for(four, listing)
        hold_two = Reservation.request_hold(two, listing, two.requester)
        hold_two.confirm(self.users["eng.custodian"])
        self.complete(transfer, 4)
        listing.refresh_from_db()
        self.assertNotEqual(listing.status, Listing.Status.CLOSED)
        # The units that moved keep their furniture details.
        self.assertTrue(FurnitureAsset.objects.filter(pk=transfer.received_asset_id).exists())

    def test_carbon_counts_only_confirmed_avoided_purchases(self):
        start = timezone.localdate().replace(month=1, day=1)
        before = SustainabilityIndicators(start, timezone.localdate()).totals()
        listing = Listing.objects.get(asset__name__startswith="Ergonomic")
        self.complete(self.transfer_for(self.new_request("Chairs", listing.asset.category, quantity=2), listing), 2)
        after = SustainabilityIndicators(start, timezone.localdate()).totals()
        self.assertEqual(after["items_reused"], before["items_reused"] + 2)
        self.assertEqual(after["co2e_low_kg"], before["co2e_low_kg"])  # not confirmed yet

    def test_an_avoided_purchase_is_confirmed_once(self):
        listing = Listing.objects.get(asset__name__startswith="Ergonomic")
        transfer = self.complete(self.transfer_for(self.new_request("Chairs", listing.asset.category, 2), listing), 2)
        impact = SustainabilityImpact.objects.get(transfer=transfer)
        start = timezone.localdate().replace(month=1, day=1)
        before = SustainabilityIndicators(start, timezone.localdate()).totals()
        impact.confirm_avoided_purchase(self.users["comp.rep"])
        with self.assertRaisesMessage(BusinessRuleError, "already confirmed"):
            impact.confirm_avoided_purchase(self.users["comp.rep"])
        after = SustainabilityIndicators(start, timezone.localdate()).totals()
        # Chairs have no cited replacement cost: the request counts, the net savings do not drop.
        self.assertEqual(after["avoided_purchase_requests"], before["avoided_purchase_requests"] + 1)
        self.assertEqual(after["net_savings_aed"], before["net_savings_aed"])
        self.assertEqual(after["requests_without_price"], 1)
        self.assertGreater(after["co2e_low_kg"], before["co2e_low_kg"])

    def test_every_refused_page_is_logged(self):
        other = Asset.objects.filter(owner_department__code="COMP").first()
        self.assertEqual(self.sign_in("eng.rep").get(f"/assets/{other.pk}/").status_code, 403)
        self.assertTrue(AuditLog.objects.filter(action="blocked: open record", reason=f"/assets/{other.pk}/").exists())

    def test_a_tampered_hold_request_is_not_a_server_error(self):
        response = self.sign_in("comp.requester").post("/transfers/holds/request/", {"listing": "abc", "request": "x"})
        self.assertEqual(response.status_code, 404)

    def test_a_not_working_item_cannot_be_offered(self):
        oscilloscope = Asset.objects.get(name="Digital oscilloscope")
        oscilloscope.listings.update(status=Listing.Status.WITHDRAWN)
        Asset.objects.filter(pk=oscilloscope.pk).update(condition=Condition.NOT_WORKING)
        oscilloscope.refresh_from_db()
        listing = Listing.objects.create(asset=oscilloscope, quantity=1, created_by=self.users["eng.custodian"])
        with self.assertRaisesMessage(BusinessRuleError, "Not working"):
            listing.submit_for_release(self.users["eng.custodian"])

    def test_the_representative_gets_a_link_to_the_approval_task(self):
        chairs = ResourceRequest.objects.get(purpose__startswith="Chairs")
        rep = self.sign_in("comp.rep")
        self.assertContains(rep.get(f"/requests/{chairs.pk}/"), f"/transfers/approvals/{chairs.approvals.get().pk}/")
        cards = self.sign_in("eng.rep").get("/").context["cards"]
        release = next(c for c in cards if "Listings to release" in str(c))
        self.assertIn("/transfers/approvals/", str(release))

    def test_a_second_start_of_the_same_hold_opens_the_transfer(self):
        listing = Listing.objects.get(asset__name__startswith="Epson")
        request = ResourceRequest.objects.get(purpose__startswith="Projector")
        transfer = self.transfer_for(request, listing)
        response = self.sign_in("comp.requester").get(f"/transfers/holds/{transfer.reservation_id}/start/")
        self.assertRedirects(response, f"/transfers/{transfer.pk}/", fetch_redirect_response=False)
