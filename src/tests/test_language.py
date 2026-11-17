"""English and Arabic: the language button, right to left, and notifications in each person's language."""

from django.conf import settings
from django.contrib.staticfiles import finders

from accounts.models import User
from notifications.models import Notification
from resource_requests.models import ResourceRequest

from .helpers import DemoTestCase


class LanguageTests(DemoTestCase):
    def test_the_header_button_switches_to_arabic_and_saves_it(self):
        client = self.sign_in("comp.requester")
        response = client.post("/accounts/settings/language/", {"language": "ar", "next": "/requests/"})
        self.assertRedirects(response, "/requests/", fetch_redirect_response=False)
        self.assertEqual(response.cookies[settings.LANGUAGE_COOKIE_NAME].value, "ar")
        self.assertEqual(User.objects.get(username="comp.requester").language, "ar")
        page = client.get("/requests/").content.decode()
        self.assertIn('lang="ar" dir="rtl"', page)
        self.assertIn("dawra/rtl/styles.css", page)
        self.assertIn("تسجيل الخروج", page)  # "Sign out"

    def test_english_stays_left_to_right(self):
        page = self.sign_in("comp.requester").get("/").content.decode()
        self.assertIn('lang="en-gb" dir="ltr"', page)
        self.assertNotIn("dawra/rtl/", page)

    def test_the_sign_in_page_can_switch_before_signing_in(self):
        self.client.post("/accounts/settings/language/", {"language": "ar", "next": "/accounts/sign-in/"})
        self.assertContains(self.client.get("/accounts/sign-in/"), 'dir="rtl"')

    def test_an_unknown_language_falls_back_to_english(self):
        client = self.sign_in("comp.requester")
        client.post("/accounts/settings/language/", {"language": "xx"})
        self.assertEqual(User.objects.get(username="comp.requester").language, "en-gb")

    def test_each_person_gets_notifications_in_their_own_language(self):
        User.objects.filter(username="comp.requester").update(language="ar")
        request = ResourceRequest.objects.get(purpose__startswith="Chairs")
        self.sign_in("comp.rep").post(f"/transfers/approvals/{request.approvals.get().pk}/",
                                      {"decision": "approve", "reason": ""})
        message = Notification.objects.filter(user__username="comp.requester").latest("pk").message
        self.assertRegex(message, "[؀-ۿ]")  # Arabic letters

    def test_history_is_saved_in_english_and_shown_in_the_readers_language(self):
        from audit.models import AuditLog
        from audit.templatetags.audit_ui import localized
        from django.utils import translation

        User.objects.filter(username="comp.rep").update(language="ar")
        request = ResourceRequest.objects.get(purpose__startswith="Chairs")
        self.sign_in("comp.rep").post(f"/transfers/approvals/{request.approvals.get().pk}/",
                                      {"decision": "approve", "reason": ""})
        entry = AuditLog.objects.filter(record_type="resourcerequest", record_id=request.pk).latest("pk")
        self.assertEqual(entry.after_value, "RQ-03 Open")  # saved in English
        self.assertNotRegex(entry.role, "[؀-ۿ]")
        with translation.override("ar"):
            self.assertRegex(str(localized(entry.after_value)), "^RQ-03 [؀-ۿ]")

    def test_the_right_to_left_and_arabic_files_exist(self):
        for name in ("rtl/styles.css", "rtl/app.css", "rtl/ui.css", "rtl/dark.css", "rtl/effects.css",
                     "rtl/motion.css", "arabic.css"):
            self.assertIsNotNone(finders.find(f"dawra/{name}"), name)
