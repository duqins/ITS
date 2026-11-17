"""Small things found when walking through the demo as a tester."""

import re

from django.utils import translation

from accounts.models import User
from audit.templatetags.audit_ui import action_text
from resource_requests.models import ResourceRequest
from transfers.models import Transfer

from .helpers import DemoTestCase

ARABIC = "[؀-ۿ]"


class WalkthroughFixTests(DemoTestCase):
    def test_a_finished_request_and_transfer_show_every_stage_as_done(self):
        fulfilled = ResourceRequest.objects.get(status=ResourceRequest.Status.FULFILLED)
        page = self.sign_in("comp.requester").get(f"/requests/{fulfilled.pk}/").content.decode()
        self.assertNotIn('class="current"', page)
        self.assertEqual(page.count('<li class="done">'), 6)
        completed = Transfer.objects.get(status=Transfer.Status.COMPLETED)
        page = self.sign_in("comp.custodian").get(f"/transfers/{completed.pk}/").content.decode()
        self.assertNotIn('class="current"', page)

    def test_handover_and_receipt_times_use_the_same_format_as_the_history(self):
        completed = Transfer.objects.get(status=Transfer.Status.COMPLETED)
        page = self.sign_in("comp.custodian").get(f"/transfers/{completed.pk}/").content.decode()
        self.assertNotRegex(page, r"\d (a\.m\.|p\.m\.)")
        self.assertRegex(page, r"\d\d \w{3} \d{4} \d\d:\d\d GST")  # SRS 3.1.1: DD Mon YYYY, time zone shown

    def test_report_dates_read_like_other_dates_and_the_csv_keeps_iso_dates(self):
        client = self.sign_in("business.admin")
        page = client.get("/reports/").content.decode()
        self.assertNotRegex(page, r"<td>\d{4}-\d\d-\d\d</td>")
        csv = client.get("/reports/?format=csv").content.decode()
        self.assertRegex(csv, r",\d{4}-\d\d-\d\d\r?\n")

    def test_the_report_department_filter_is_translated(self):
        User.objects.filter(username="business.admin").update(language="ar")
        page = self.sign_in("business.admin").get("/reports/").content.decode()
        label = re.search(r'<label for="id_department">([^<]*)</label>', page).group(1)
        self.assertRegex(label, ARABIC)

    def test_history_lines_with_a_code_or_a_refused_action_are_translated(self):
        with translation.override("en-gb"):
            self.assertEqual(action_text("1 unit(s) moved to AST-0007"), "1 unit moved to AST-0007")
            self.assertEqual(action_text("2 units moved to AST-0007"), "2 units moved to AST-0007")
            self.assertEqual(action_text("blocked: request hold"), "blocked: request hold")
            self.assertEqual(action_text("AI classification suggestion accepted"),
                             "AI classification suggestion accepted")
        with translation.override("ar"):
            for line in ("1 unit moved to AST-0007", "received from AST-0003 by TRF-0002",
                         "AI match AST-0003 rejected", "AI classification suggestion corrected",
                         "blocked: request hold"):
                text = str(action_text(line))
                self.assertRegex(text, ARABIC, line)
                self.assertNotRegex(text, r"\b(unit|received|match|suggestion|blocked|request)\b", line)
            self.assertIn("AST-0007", action_text("1 unit moved to AST-0007"))

    def test_money_has_thousands_separators_in_both_languages(self):
        from assets.models import Asset
        asset = Asset.objects.filter(value__gte=1000, owner_department__code="ENG").first()
        for language in ("en-gb", "ar"):
            User.objects.filter(username="eng.custodian").update(language=language)
            page = self.sign_in("eng.custodian").get(f"/assets/{asset.pk}/").content.decode()
            self.assertRegex(page, r"\d,\d{3}\.\d\d", language)

    def test_one_ranked_item_is_singular(self):
        from django.utils.translation import ngettext
        with translation.override("en-gb"):
            text = ngettext("%(count)s eligible item ranked.", "%(count)s eligible items ranked.", 1) % {"count": 1}
        self.assertEqual(text, "1 eligible item ranked.")

    def test_forms_tell_the_browser_the_same_limits_as_the_server(self):
        page = self.sign_in("comp.requester").get("/requests/new/").content.decode()
        self.assertRegex(page, r'name="quantity"[^>]*min="1"')
        self.assertRegex(page, r'name="required_by"[^>]*min="\d{4}-\d\d-\d\d"')
        self.assertIn("Choose a category", page)

    def test_the_required_note_is_marked_so_pages_without_fields_can_hide_it(self):
        page = self.sign_in("comp.requester").get("/").content.decode()
        self.assertIn('class="required-note"', page)

    def test_a_missing_page_keeps_the_app_around_it(self):
        response = self.sign_in("comp.requester").get("/assets/new/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "We could not find that page", status_code=404)
        self.assertContains(response, "Back to the home page", status_code=404)

    def test_the_server_error_page_needs_nothing_that_could_fail(self):
        from django.template.loader import get_template
        page = get_template("500.html").render()
        self.assertIn("Something went wrong on our side", page)
        self.assertIn("حدث خطأ من جهتنا", page)

    def test_a_wrong_password_marks_the_sign_in_card(self):
        page = self.client.post("/accounts/sign-in/", {"username": "comp.requester", "password": "wrong"})
        self.assertContains(page, 'class="signin-card refused"')


class ReviewerFixTests(DemoTestCase):
    """What an independent tester found by walking through the demo script."""

    def projector_request(self):
        return ResourceRequest.objects.get(purpose__startswith="Projector")

    def test_a_hold_needs_the_right_category_condition_and_date(self):
        from assets.models import Listing
        chairs = Listing.objects.get(asset__name__startswith="Ergonomic")
        client = self.sign_in("comp.requester")
        page = client.get(f"/assets/listings/{chairs.pk}/").content.decode()
        self.assertNotIn(self.projector_request().code, page)  # not offered for a chair
        client.post("/transfers/holds/request/", {"request": self.projector_request().pk, "listing": chairs.pk})
        self.assertEqual(self.projector_request().status, ResourceRequest.Status.OPEN)  # and refused on the server

    def test_a_refused_publish_keeps_the_edited_summary(self):
        from unittest import mock

        from ai.models import AiSuggestion
        from ai.report_drafts import ReportAnswer

        from .helpers import FakeClaude
        officer = self.sign_in("sustainability.officer")
        fake = FakeClaude({ReportAnswer: lambda p: ReportAnswer(summary="2 items were reused.")})
        with self.settings(ANTHROPIC_API_KEY="test-key"), mock.patch("ai.adapter.anthropic.Anthropic", return_value=fake):
            officer.post("/ai/report/draft/")
            draft = AiSuggestion.objects.get(task="report")
            officer.post(f"/ai/report/{draft.pk}/publish/",
                         {"summary": "My own words, and 999 items.", "decision": "publish", "next": "/sustainability/"})
            page = officer.get("/sustainability/").content.decode()
        self.assertIn("My own words, and 999 items.", page)
        self.assertIn("999", page)

    def test_editing_a_draft_shows_its_own_custodian(self):
        from assets.models import Asset
        asset = Asset.objects.filter(owner_department__code="ENG", custodian__username="eng.custodian").first()
        asset.pk = asset.id = None
        asset.status = Asset.Status.DRAFT
        asset.save()
        page = self.sign_in("eng.rep").get(f"/assets/{asset.pk}/edit/").content.decode()
        custodian = re.search(r'Custodian</span><div class="readonly">([^<]*)<', page).group(1)
        self.assertEqual(custodian, "Khalid Al Mansoori")

    def test_help_and_error_texts_have_the_ids_the_inputs_point_to(self):
        page = self.sign_in("comp.requester").post("/requests/new/", {"purpose": ""}).content.decode()
        for described in re.findall(r'aria-describedby="([^"]+)"', page):
            for target in described.split():
                self.assertIn(f'id="{target}"', page, target)

    def test_a_missing_building_earns_no_location_points(self):
        from ai.matching import RankingModel
        listing = self.projector_request().category.assets.first().listings.first()
        listing.asset.building = ""
        factors = RankingModel().score(self.projector_request(), listing, 0.5)[1]
        location = next(f for f in factors if f["max"] == 10 and "building" in f["used"].lower())
        self.assertEqual(location["points"], 0)
        self.assertTrue(location["unknown"])

    def test_refused_attempts_stay_in_the_audit_log_but_not_on_the_request(self):
        from audit.models import AuditLog
        request = self.projector_request()
        AuditLog.record(User.objects.get(username="comp.rep"), "blocked: decide approval", request, reason="BR-20")
        page = self.sign_in("comp.requester").get(f"/requests/{request.pk}/").content.decode()
        self.assertNotIn("Blocked", page)
        self.assertTrue(AuditLog.objects.filter(action="blocked: decide approval").exists())

    def test_the_next_step_and_where_a_request_stopped_are_shown(self):
        pending = ResourceRequest.objects.get(status=ResourceRequest.Status.PENDING_APPROVAL)
        page = self.sign_in("comp.requester").get(f"/requests/{pending.pk}/").content.decode()
        self.assertIn("Next step", page)
        self.assertIn("department representative approves it", page)
        approval = pending.approvals.get()
        self.sign_in("comp.rep").post(f"/transfers/approvals/{approval.pk}/", {"decision": "reject", "reason": "No budget"})
        page = self.sign_in("comp.requester").get(f"/requests/{pending.pk}/").content.decode()
        self.assertIn('class="stopped"', page)
        self.assertEqual(page.count('<li class="done">'), 1)  # stopped at department review, after the draft

    def test_consequential_buttons_ask_first_and_history_shows_record_codes(self):
        pending = ResourceRequest.objects.get(status=ResourceRequest.Status.PENDING_APPROVAL)
        page = self.sign_in("comp.rep").get(f"/transfers/approvals/{pending.approvals.get().pk}/").content.decode()
        self.assertEqual(page.count("data-confirm="), 3)  # approve, request changes, reject
        self.assertIn(pending.code, re.search(r'value="approve" data-confirm="([^"]*)"', page).group(1))
        log = self.sign_in("business.admin").get("/history/audit-log/").content.decode()
        self.assertRegex(log, r"<td>(AST|LST|REQ|HLD|TRF)-\d{4}</td>")
        self.assertNotRegex(log, r"<td>(Asset|Transfer|Request|Listing) \d+</td>")

    def test_the_home_page_shows_what_ui_02_lists(self):
        page = self.sign_in("sustainability.officer").get("/").content.decode()
        self.assertIn("Unread notifications", page)
        page = self.sign_in("comp.rep").get("/").content.decode()
        self.assertIn("Overdue tasks", page)
        self.assertIn("Approval tasks", page)
        page = self.sign_in("comp.requester").get("/").content.decode()
        self.assertIn("Holds ending soon", page)
