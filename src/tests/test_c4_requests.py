"""C4 Request and track."""

from datetime import date, timedelta

from assets.models import Category
from resource_requests.models import ResourceRequest

from .helpers import DemoTestCase


class RequestTests(DemoTestCase):
    def data(self, **extra):
        values = {"purpose": "Monitor for a TA desk", "category": Category.objects.get(subcategory="Monitor").pk,
                  "quantity": 1, "min_condition": "fair", "urgency": "normal", "required_by": self.future(),
                  "submit_for": "approval", "specifications": "24-inch, HDMI", "delivery_location": "Computing Building C1-001",}
        values.update(extra)
        return values

    def test_staff_submit_a_request_and_see_its_status(self):
        client = self.sign_in("comp.requester")
        response = client.post("/requests/new/", self.data(), follow=True)
        request = ResourceRequest.objects.get(purpose="Monitor for a TA desk")
        self.assertEqual(request.status, ResourceRequest.Status.PENDING_APPROVAL)
        self.assertContains(response, "Pending department approval")
        self.assertContains(client.get("/requests/"), "Monitor for a TA desk")

    def test_required_by_date_in_the_past_is_refused(self):
        past = (date.today() - timedelta(days=1)).isoformat()
        response = self.sign_in("comp.requester").post("/requests/new/", self.data(required_by=past))
        self.assertContains(response, "today or later")

    def test_requester_only_sees_own_requests(self):
        self.sign_in("comp.requester").post("/requests/new/", self.data())
        request = ResourceRequest.objects.get(purpose="Monitor for a TA desk")
        self.assertEqual(self.sign_in("eng.custodian").get(f"/requests/{request.pk}/").status_code, 403)

    def test_cancel_needs_a_reason(self):
        client = self.sign_in("comp.requester")
        open_request = ResourceRequest.objects.get(purpose__startswith="Projector")
        client.post(f"/requests/{open_request.pk}/cancel/", {"reason": ""})
        open_request.refresh_from_db()
        self.assertEqual(open_request.status, ResourceRequest.Status.OPEN)
        client.post(f"/requests/{open_request.pk}/cancel/", {"reason": "Not needed any more"})
        open_request.refresh_from_db()
        self.assertEqual(open_request.status, ResourceRequest.Status.CANCELLED)
