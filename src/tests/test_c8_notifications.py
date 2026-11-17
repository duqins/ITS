"""C8 Notifications: in-app messages when a request is made, approved, rejected or received."""

from accounts.models import User
from assets.models import Category
from notifications.models import Notification
from resource_requests.models import ResourceRequest

from .helpers import DemoTestCase


class NotificationTests(DemoTestCase):
    def test_request_made_notifies_the_department_representative(self):
        self.sign_in("comp.requester").post("/requests/new/", {
            "purpose": "Laptop for an intern", "category": Category.objects.get(subcategory="Laptop").pk,
            "quantity": 1, "min_condition": "fair", "urgency": "normal", "required_by": self.future(),
            "submit_for": "approval", "specifications": "24-inch, HDMI", "delivery_location": "Computing Building C1-001",})
        rep = User.objects.get(username="comp.rep")
        self.assertTrue(rep.notifications.filter(message__contains="New approval task").exists())

    def test_approved_and_rejected_reach_the_requester(self):
        rep = User.objects.get(username="comp.rep")
        chairs = ResourceRequest.objects.get(purpose__startswith="Chairs")
        chairs.reject(rep, "No budget for moving furniture")
        requester = chairs.requester
        self.assertTrue(requester.notifications.filter(message__contains="was rejected").exists())
        approved = ResourceRequest.objects.get(purpose__startswith="Projector")
        self.assertTrue(requester.notifications.filter(record_id=approved.pk, message__contains="approved").exists())

    def test_receipt_reaches_the_requester(self):
        requester = User.objects.get(username="comp.requester")
        self.assertTrue(requester.notifications.filter(message__contains="was received by Computing").exists())

    def test_unread_count_and_mark_as_read(self):
        client = self.sign_in("comp.requester")
        unread = Notification.objects.filter(user__username="comp.requester", read_at__isnull=True)
        count = unread.count()
        self.assertGreater(count, 0)
        self.assertContains(client.get("/"), f"{count} unread notification")
        first = unread.first()
        client.get(f"/notifications/{first.pk}/open/")
        first.refresh_from_db()
        self.assertTrue(first.is_read)

    def test_users_only_open_their_own_notifications(self):
        other = Notification.objects.exclude(user__username="eng.rep").first()
        self.assertEqual(self.sign_in("eng.rep").get(f"/notifications/{other.pk}/open/").status_code, 404)

    def test_a_request_opened_again_is_not_called_approved(self):
        rep, custodian = User.objects.get(username="comp.rep"), User.objects.get(username="eng.custodian")
        request = ResourceRequest.objects.get(purpose__startswith="Projector")
        from assets.models import Listing
        from transfers.models import Reservation
        hold = Reservation.request_hold(request, Listing.objects.get(asset__name__startswith="Epson"), request.requester)
        before = request.requester.notifications.filter(message__contains="approved").count()
        hold.decline(custodian, "Still in use")
        self.assertEqual(request.requester.notifications.filter(message__contains="approved").count(), before)
        self.assertTrue(request.requester.notifications.filter(message__contains="was declined").exists())
        self.assertIsNotNone(rep)
