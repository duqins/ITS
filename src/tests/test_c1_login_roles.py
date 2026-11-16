"""C1 Login and roles: at least 3 roles, and the server checks permissions."""

from accounts.models import Role, User
from assets.models import Listing
from audit.models import AuditLog

from .helpers import PASSWORD, DemoTestCase


class LoginAndRolesTests(DemoTestCase):
    def test_nine_roles_exist(self):
        self.assertEqual(Role.objects.count(), 9)

    def test_pages_need_sign_in(self):
        response = self.client.get("/assets/search/")
        self.assertRedirects(response, "/accounts/sign-in/?next=/assets/search/")

    def test_five_wrong_passwords_lock_the_account(self):
        for _ in range(5):
            self.client.post("/accounts/sign-in/", {"username": "eng.rep", "password": "wrong"})
        response = self.client.post("/accounts/sign-in/", {"username": "eng.rep", "password": PASSWORD})
        self.assertContains(response, "locked")
        self.assertTrue(User.objects.get(username="eng.rep").is_locked())

    def test_server_refuses_an_action_the_role_does_not_allow(self):
        listing = Listing.objects.first()
        requester = self.sign_in("comp.requester")
        response = requester.post(f"/assets/listings/{listing.pk}/decide/", {"decision": "approve"})
        self.assertEqual(response.status_code, 403)
        self.assertTrue(AuditLog.objects.filter(action="blocked: listing.publish").exists())

    def test_refused_page_offers_the_users_other_role_and_returns_to_the_page(self):
        from transfers.models import Approval
        representative = User.objects.get(username="comp.rep").user_roles.get(role__code="department_representative")
        approval = Approval.objects.filter(department=representative.department).first()
        rep = self.sign_in("comp.rep", role="requester")
        path = f"/transfers/approvals/{approval.pk}/"
        refused = rep.get(path)
        self.assertEqual(refused.status_code, 403)
        self.assertContains(refused, f"Switch to {representative} and try again", status_code=403)
        switched = rep.post("/accounts/switch-role/", {"user_role": representative.pk, "next": path})
        self.assertRedirects(switched, path, fetch_redirect_response=False)
        self.assertEqual(rep.get(path).status_code, 200)
        outside = rep.post("/accounts/switch-role/", {"user_role": representative.pk, "next": "https://example.com/"})
        self.assertRedirects(outside, "/", fetch_redirect_response=False)

    def test_switching_role_changes_what_the_server_allows(self):
        rep = self.sign_in("comp.rep")
        self.assertEqual(rep.get("/requests/new/").status_code, 403)
        rep = self.sign_in("comp.rep", role="requester")
        self.assertEqual(rep.get("/requests/new/").status_code, 200)

    def test_menu_hides_sections_the_role_cannot_use(self):
        response = self.sign_in("comp.requester").get("/")
        self.assertNotContains(response, "Audit log")
        self.assertContains(self.sign_in("business.admin").get("/"), "Audit log")
