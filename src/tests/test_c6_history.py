"""C6 States and history: only the moves of the state diagrams, and who did what, when."""

from accounts.models import User
from assets.models import Asset
from audit.lifecycle import TransitionNotAllowed
from audit.models import AuditLog
from resource_requests.models import ResourceRequest

from .helpers import DemoTestCase


class StateRuleTests(DemoTestCase):
    def test_moves_outside_the_cycle_are_refused(self):
        asset = Asset.objects.get(name="Digital oscilloscope")  # In storage
        with self.assertRaises(TransitionNotAllowed):
            asset.change_status(Asset.Status.DONATED, User.objects.get(username="eng.rep"))
        fulfilled = ResourceRequest.objects.get(status=ResourceRequest.Status.FULFILLED)
        with self.assertRaises(TransitionNotAllowed):
            fulfilled.close_no_suitable_item(fulfilled.requester, "too late")

    def test_every_state_change_is_logged(self):
        asset = Asset.objects.get(name="Digital oscilloscope")
        entries = AuditLog.for_record(asset)
        self.assertTrue(entries.filter(action="registered", user__username="eng.custodian").exists())
        self.assertTrue(entries.filter(action="confirmed", user__username="eng.rep", after_value="AS-03 In storage").exists())

    def test_audit_entries_cannot_be_changed_or_deleted(self):
        entry = AuditLog.objects.first()
        entry.reason = "edited"
        with self.assertRaises(ValueError):
            entry.save()
        with self.assertRaises(ValueError):
            entry.delete()

    def test_history_page_shows_who_did_what_and_when(self):
        monitors = Asset.objects.get(name__startswith="Dell", owner_department__code="ENG")
        response = self.sign_in("eng.rep").get(f"/history/asset/{monitors.pk}/")
        self.assertContains(response, "Hold confirmed")
        self.assertContains(response, "Khalid Al Mansoori")
        self.assertEqual(self.sign_in("comp.rep").get(f"/history/asset/{monitors.pk}/").status_code, 403)

    def test_audit_log_search_and_csv_for_the_business_administrator(self):
        admin = self.sign_in("business.admin")
        self.assertContains(admin.get("/history/audit-log/?action=confirmed"), "Confirmed")
        response = admin.get("/history/audit-log/?format=csv")
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertEqual(self.sign_in("eng.rep").get("/history/audit-log/").status_code, 403)
