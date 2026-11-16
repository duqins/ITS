"""C5 Approve and transfer: approval with no self-approval, receiver confirms, owner and department
change, and the last item cannot go to two people."""

from datetime import date

from accounts.models import User
from assets.models import Asset, Category, Listing
from audit.lifecycle import BusinessRuleError
from resource_requests.models import ResourceRequest
from transfers.models import Reservation, Transfer

from .helpers import DemoTestCase


class TransferFlowTests(DemoTestCase):
    def setUp(self):
        self.requester = self.sign_in("comp.requester")
        self.comp_rep, self.eng_rep = self.sign_in("comp.rep"), self.sign_in("eng.rep")
        self.eng_cust, self.comp_cust = self.sign_in("eng.custodian"), self.sign_in("comp.custodian")

    def decide(self, client, approval, decision="approve", reason=""):
        return client.post(f"/transfers/approvals/{approval.pk}/", {"decision": decision, "reason": reason}, follow=True)

    def start_chairs_transfer(self):
        request = ResourceRequest.objects.get(purpose__startswith="Chairs")
        self.decide(self.comp_rep, request.approvals.get())
        listing = Listing.objects.get(asset__name__startswith="Ergonomic")
        self.requester.post("/transfers/holds/request/", {"request": request.pk, "listing": listing.pk})
        hold = Reservation.objects.get(request=request)
        self.eng_cust.post(f"/transfers/holds/{hold.pk}/decide/", {"decision": "confirm"})
        self.requester.post(f"/transfers/holds/{hold.pk}/start/", {
            "to_custodian": User.objects.get(username="comp.custodian").pk, "to_building": "Computing Building",
            "delivery_arrangement": "delivery", "distance_km": "5", "van_trips": "1", "transfer_cost_aed": "60",
            "planned_date": date.today().isoformat()})
        return request, Transfer.objects.get(reservation=hold)

    def test_full_transfer_changes_owner_and_department_on_receipt(self):
        request, transfer = self.start_chairs_transfer()
        self.decide(self.eng_rep, transfer.approvals.get(status="AT-01"))
        self.decide(self.comp_rep, transfer.approvals.get(status="AT-01"))
        transfer.refresh_from_db()
        self.assertEqual(transfer.status, Transfer.Status.APPROVED)
        self.eng_cust.post(f"/transfers/{transfer.pk}/hand-over/", {"condition": "fair"})
        transfer.refresh_from_db()
        self.assertEqual(transfer.asset.owner_department.code, "ENG")  # nothing changes before receipt
        self.comp_cust.post(f"/transfers/{transfer.pk}/receive/", {"received_quantity": 4, "received_condition": "fair",
                                                                   "outcome": "ok"})
        transfer.refresh_from_db()
        request.refresh_from_db()
        self.assertEqual(transfer.status, Transfer.Status.COMPLETED)
        self.assertEqual(request.status, ResourceRequest.Status.FULFILLED)
        self.assertEqual(transfer.received_asset.owner_department.code, "COMP")
        self.assertEqual(transfer.received_asset.custodian.username, "comp.custodian")
        self.assertEqual(transfer.received_asset.quantity, 4)

    def test_no_self_approval(self):
        rep_as_requester = self.sign_in("comp.rep", role="requester")
        rep_as_requester.post("/requests/new/", {
            "purpose": "Own monitor", "category": Category.objects.get(subcategory="Monitor").pk, "quantity": 1,
            "min_condition": "fair", "urgency": "normal", "required_by": self.future(), "submit_for": "approval"})
        own = ResourceRequest.objects.get(purpose="Own monitor")
        response = self.decide(self.comp_rep, own.approvals.get())
        own.refresh_from_db()
        self.assertEqual(own.status, ResourceRequest.Status.PENDING_APPROVAL)
        self.assertTrue(any("own" in e for e in self.errors(response)))

    def test_other_department_cannot_approve_and_reject_needs_reason(self):
        request = ResourceRequest.objects.get(purpose__startswith="Chairs")
        self.assertEqual(self.eng_rep.get(f"/transfers/approvals/{request.approvals.get().pk}/").status_code, 403)
        self.decide(self.comp_rep, request.approvals.get(), "reject", "")
        request.refresh_from_db()
        self.assertEqual(request.status, ResourceRequest.Status.PENDING_APPROVAL)

    def test_receiver_must_record_a_discrepancy_when_the_quantity_differs(self):
        _, transfer = self.start_chairs_transfer()
        self.decide(self.eng_rep, transfer.approvals.get(status="AT-01"))
        self.decide(self.comp_rep, transfer.approvals.get(status="AT-01"))
        self.eng_cust.post(f"/transfers/{transfer.pk}/hand-over/", {"condition": "fair"})
        self.comp_cust.post(f"/transfers/{transfer.pk}/receive/", {"received_quantity": 3, "received_condition": "fair",
                                                                   "outcome": "ok"})
        transfer.refresh_from_db()
        self.assertEqual(transfer.status, Transfer.Status.HANDED_OVER)
        self.comp_cust.post(f"/transfers/{transfer.pk}/receive/", {"received_quantity": 3, "received_condition": "fair",
                                                                   "outcome": "discrepancy", "note": "One chair missing"})
        transfer.refresh_from_db()
        self.assertEqual(transfer.status, Transfer.Status.DISPUTED)

    def test_high_value_procurement_item_needs_policy_approval(self):
        request = ResourceRequest.objects.create(
            purpose="Oscilloscope", category=Category.objects.get(subcategory="Measurement"), quantity=1,
            min_condition="fair", required_by=date.today().replace(year=date.today().year + 1),
            requester=User.objects.get(username="comp.requester"), department=User.objects.get(username="comp.rep").department)
        request.submit(request.requester)
        request.approve(User.objects.get(username="comp.rep"))
        hold = Reservation.request_hold(request, Listing.objects.get(asset__name="Digital oscilloscope"), request.requester)
        hold.confirm(User.objects.get(username="eng.custodian"))
        transfer = Transfer.start(hold, request.requester, User.objects.get(username="comp.custodian"))
        transfer.approve_stage(User.objects.get(username="eng.rep"))
        transfer.approve_stage(User.objects.get(username="comp.rep"))
        self.assertEqual(transfer.status, Transfer.Status.PENDING_POLICY)
        self.assertEqual(set(transfer.pending_approvals().values_list("stage", flat=True)),
                         {"transfer_finance", "transfer_procurement"})

    def test_the_last_item_cannot_go_to_two_people(self):
        listing = Listing.objects.get(asset__name__startswith="Epson")
        first = ResourceRequest.objects.get(purpose__startswith="Projector")
        second = ResourceRequest.objects.create(
            purpose="Second projector", category=first.category, quantity=1, min_condition="poor",
            required_by=first.required_by, requester=User.objects.get(username="comp.rep"), department=first.department,
            status=ResourceRequest.Status.OPEN)
        hold_a = Reservation.request_hold(first, listing, first.requester)
        hold_b = Reservation.request_hold(second, listing, second.requester)
        custodian = User.objects.get(username="eng.custodian")
        hold_a.confirm(custodian)
        with self.assertRaises(BusinessRuleError):
            hold_b.confirm(custodian)
        asset = Asset.objects.get(pk=listing.asset_id)
        self.assertEqual((asset.available_qty, asset.reserved_qty), (0, 1))
