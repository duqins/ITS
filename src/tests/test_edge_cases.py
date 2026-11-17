"""Edge cases of holds, transfers and listings found while testing before the demo."""

from datetime import date, timedelta
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from accounts.models import User
from assets.models import Asset, Category, Condition, Listing
from audit.lifecycle import BusinessRuleError
from audit.models import AuditLog
from resource_requests.models import ResourceRequest
from transfers.models import Approval, Reservation, Transfer, expire_overdue

from .helpers import DemoTestCase


class EdgeCaseTests(DemoTestCase):
    def setUp(self):
        self.users = {u.username: u for u in User.objects.all()}

    def new_request(self, purpose, category, quantity=1, minimum=Condition.POOR, requester="comp.requester"):
        request = ResourceRequest.objects.create(
            purpose=purpose, category=category, quantity=quantity, min_condition=minimum,
            required_by=date.today() + timedelta(days=20), requester=self.users[requester],
            department=self.users[requester].department)
        request.submit(request.requester)
        rep = self.users["comp.rep"] if requester != "comp.rep" else None
        if rep:
            request.approve(rep)
        else:
            request.status = ResourceRequest.Status.OPEN
            request.save(update_fields=["status"])
        return request

    def transfer_for(self, request, listing):
        hold = Reservation.request_hold(request, listing, request.requester)
        hold.confirm(self.users["eng.custodian"])
        return Transfer.start(hold, request.requester, self.users["comp.custodian"])

    def test_a_rejected_transfer_gives_the_units_back_to_the_listing(self):
        listing = Listing.objects.get(asset__name__startswith="Epson")
        request = ResourceRequest.objects.get(purpose__startswith="Projector")
        transfer = self.transfer_for(request, listing)
        transfer.reject_stage(self.users["eng.rep"], "Still needed in Engineering")
        listing.refresh_from_db()
        self.assertEqual(listing.status, Listing.Status.PUBLISHED)
        self.assertEqual(listing.remaining_quantity(), 1)

    def test_a_listing_cannot_hold_more_than_was_released(self):
        chairs = Asset.objects.get(name__startswith="Ergonomic")
        listing = chairs.listings.get()
        Listing.objects.filter(pk=listing.pk).update(quantity=2)  # 6 chairs, but only 2 released
        listing.refresh_from_db()
        category = chairs.category
        first = self.new_request("Two chairs", category, quantity=2)
        second = self.new_request("Two more chairs", category, quantity=2, requester="comp.rep")
        hold_a = Reservation.request_hold(first, listing, first.requester)
        hold_b = Reservation.request_hold(second, listing, second.requester)
        hold_a.confirm(self.users["eng.custodian"])
        with self.assertRaises(BusinessRuleError):
            hold_b.confirm(self.users["eng.custodian"])

    def test_closing_a_listing_cancels_the_holds_still_waiting(self):
        listing = Listing.objects.get(asset__name__startswith="Epson")
        first = ResourceRequest.objects.get(purpose__startswith="Projector")
        second = self.new_request("Spare projector", first.category, requester="comp.rep")
        waiting = Reservation.request_hold(second, listing, second.requester)
        transfer = self.transfer_for(first, listing)
        transfer.approve_stage(self.users["eng.rep"])
        transfer.approve_stage(self.users["comp.rep"])
        transfer.hand_over(self.users["eng.custodian"], Condition.POOR)
        transfer.confirm_receipt(self.users["comp.custodian"], 1, Condition.POOR)
        waiting.refresh_from_db()
        second.refresh_from_db()
        self.assertEqual(waiting.status, Reservation.Status.CANCELLED)
        self.assertEqual(second.status, ResourceRequest.Status.OPEN)

    def test_two_partial_transfers_can_both_be_received(self):
        monitors = Asset.objects.get(name__startswith="Dell", owner_department__code="ENG")  # 2 left
        listing = monitors.listings.get()
        category = monitors.category
        first = self.new_request("One monitor", category)
        second = self.new_request("Another monitor", category)
        transfers = [self.transfer_for(first, listing)]
        hold = Reservation.request_hold(second, listing, second.requester)
        hold.confirm(self.users["eng.custodian"])
        transfers.append(Transfer.start(hold, second.requester, self.users["comp.custodian"]))
        for transfer in transfers:
            transfer.approve_stage(self.users["eng.rep"])
            transfer.approve_stage(self.users["comp.rep"])
            transfer.hand_over(self.users["eng.custodian"], Condition.GOOD)
        for transfer in transfers:
            transfer.confirm_receipt(self.users["comp.custodian"], 1, Condition.GOOD)
            self.assertEqual(transfer.status, Transfer.Status.COMPLETED)

    def test_editing_a_draft_quantity_keeps_every_unit_available(self):
        custodian = self.sign_in("eng.custodian")
        custodian.post("/assets/register/", {"kind": "general", "name": "Bookshelf", "condition": "good",
                                             "quantity": 1, "campus": "Main campus"})
        asset = Asset.objects.get(name="Bookshelf")
        custodian.post(f"/assets/{asset.pk}/edit/", {"name": "Bookshelf", "condition": "good", "quantity": 5,
                                                     "campus": "Main campus"})
        asset.refresh_from_db()
        self.assertEqual((asset.quantity, asset.available_qty), (5, 5))
        self.assertTrue(AuditLog.for_record(asset).filter(action="draft edited").exists())

    def test_overdue_holds_expire_and_free_the_units(self):
        listing = Listing.objects.get(asset__name__startswith="Epson")
        request = ResourceRequest.objects.get(purpose__startswith="Projector")
        hold = Reservation.request_hold(request, listing, request.requester)
        hold.confirm(self.users["eng.custodian"])
        Reservation.objects.filter(pk=hold.pk).update(expires_at=timezone.now() - timedelta(hours=1))
        expire_overdue()
        hold.refresh_from_db()
        request.refresh_from_db()
        self.assertEqual(hold.status, Reservation.Status.EXPIRED)
        self.assertEqual(request.status, ResourceRequest.Status.OPEN)
        self.assertEqual(Asset.objects.get(pk=listing.asset_id).available_qty, 1)

    def test_missing_units_cannot_be_accepted_and_received_quantity_is_limited(self):
        listing = Listing.objects.get(asset__name__startswith="Ergonomic")
        request = ResourceRequest.objects.get(purpose__startswith="Chairs")
        request.approve(self.users["comp.rep"])
        transfer = self.transfer_for(request, listing)
        transfer.approve_stage(self.users["eng.rep"])
        transfer.approve_stage(self.users["comp.rep"])
        transfer.hand_over(self.users["eng.custodian"], Condition.FAIR)
        with self.assertRaises(BusinessRuleError):
            transfer.dispute(self.users["comp.custodian"], 100, Condition.FAIR, "More arrived?")
        transfer.dispute(self.users["comp.custodian"], 3, Condition.FAIR, "One chair missing")
        with self.assertRaises(BusinessRuleError):
            transfer.resolve_dispute(self.users["comp.rep"], True, "Accept anyway")

    def test_negative_costs_are_refused(self):
        listing = Listing.objects.get(asset__name__startswith="Epson")
        request = ResourceRequest.objects.get(purpose__startswith="Projector")
        hold = Reservation.request_hold(request, listing, request.requester)
        hold.confirm(self.users["eng.custodian"])
        with self.assertRaises(BusinessRuleError):
            Transfer.start(hold, request.requester, self.users["comp.custodian"], transfer_cost_aed=Decimal("-100"))
        response = self.sign_in("comp.requester").post(f"/transfers/holds/{hold.pk}/start/", {
            "to_custodian": self.users["comp.custodian"].pk, "delivery_arrangement": "collection",
            "distance_km": "-5", "van_trips": "0", "transfer_cost_aed": "0"})
        self.assertContains(response, "cannot be negative")

    def test_finance_and_procurement_decide_in_either_order(self):
        listing = Listing.objects.get(asset__name="Digital oscilloscope")
        request = self.new_request("Oscilloscope", Category.objects.get(subcategory="Measurement"))
        transfer = self.transfer_for(request, listing)
        transfer.approve_stage(self.users["eng.rep"])
        transfer.approve_stage(self.users["comp.rep"])
        procurement = transfer.approvals.get(stage=Approval.Stage.TRANSFER_PROCUREMENT)
        response = self.sign_in("procurement.officer").post(f"/transfers/approvals/{procurement.pk}/",
                                                             {"decision": "approve"})
        procurement.refresh_from_db()
        self.assertEqual(procurement.status, Approval.Status.APPROVED)
        finance = transfer.approvals.get(stage=Approval.Stage.TRANSFER_FINANCE)
        self.sign_in("finance.officer").post(f"/transfers/approvals/{finance.pk}/", {"decision": "approve"})
        transfer.refresh_from_db()
        self.assertEqual(transfer.status, Transfer.Status.APPROVED)

    def test_a_decided_task_cannot_be_decided_again(self):
        request = ResourceRequest.objects.get(purpose__startswith="Chairs")
        approval = request.approvals.get()
        request.approve(self.users["comp.rep"])
        approval.status = Approval.Status.PENDING  # a stale copy from a second click
        with self.assertRaises(BusinessRuleError), transaction.atomic():
            approval.approve(self.users["comp.rep"])

    def test_withdrawing_a_listing_closes_its_release_task(self):
        asset = Asset.objects.get(name="Digital oscilloscope")
        listing = Listing.objects.create(asset=asset, quantity=1, created_by=self.users["eng.custodian"])
        listing.submit_for_release(self.users["eng.custodian"])
        listing.withdraw(self.users["eng.custodian"], "Not surplus after all")
        self.assertFalse(listing.approvals.filter(status=Approval.Status.PENDING).exists())
