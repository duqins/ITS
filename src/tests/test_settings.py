"""Settings: light and dark, motion, saved to the account."""

from django.contrib.staticfiles import finders

from accounts.models import User

from .helpers import DemoTestCase


class SettingsTests(DemoTestCase):
    def test_every_user_can_open_settings_and_save_them(self):
        client = self.sign_in("system.admin")
        self.assertContains(client.get("/accounts/settings/"), "Match my device")
        client.post("/accounts/settings/", {"theme": "dark", "motion": "reduced"})
        user = User.objects.get(username="system.admin")
        self.assertEqual((user.theme, user.motion), ("dark", "reduced"))
        page = client.get("/").content.decode()
        self.assertIn('data-theme="dark"', page)
        self.assertIn('data-motion="reduced"', page)

    def test_the_header_button_saves_the_theme(self):
        client = self.sign_in("comp.requester")
        response = client.post("/accounts/settings/theme/", {"theme": "light"}, HTTP_X_REQUESTED_WITH="fetch")
        self.assertEqual(response.json(), {"theme": "light"})
        self.assertEqual(User.objects.get(username="comp.requester").theme, "light")
        # Without the page script it returns to the page, never to another site.
        back = client.post("/accounts/settings/theme/", {"theme": "dark", "next": "/requests/"})
        self.assertRedirects(back, "/requests/", fetch_redirect_response=False)
        away = client.post("/accounts/settings/theme/", {"theme": "dark", "next": "https://example.com/"})
        self.assertRedirects(away, "/", fetch_redirect_response=False)

    def test_an_unknown_theme_is_ignored(self):
        client = self.sign_in("comp.requester")
        client.post("/accounts/settings/theme/", {"theme": "purple"}, HTTP_X_REQUESTED_WITH="fetch")
        self.assertEqual(User.objects.get(username="comp.requester").theme, "system")

    def test_signed_out_pages_follow_the_device(self):
        self.assertContains(self.client.get("/accounts/sign-in/"), 'data-theme="system"')

    def test_the_style_and_script_files_exist(self):
        for name in ("motion.css", "ui.css", "dark.css", "app.js"):
            self.assertIsNotNone(finders.find(f"dawra/{name}"), name)
