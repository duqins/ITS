"""Phase 7 system tests: whole workflows from the first page to the last, across several users.

The lab slides define system testing as testing the entire system against its requirements. Each
test below signs in as the demo users and does every step through the real pages, the way a person
would. No step is made to happen by calling the code behind the page. The AI is a stand-in
(FakeClaude) or switched off, so the tests need no key and no network.
"""

import re
from datetime import date
from unittest import mock

from django.test import override_settings

from accounts.models import User
from ai.adapter import ClaudeAdapter
from ai.classification import ClassificationAnswer
from ai.matching import MeaningAnswer, MeaningScore
from ai.models import AiSuggestion, MatchRecommendation
from ai.report_drafts import ReportAnswer
from assets.models import Asset, Category, Listing
from audit.models import AuditLog
from resource_requests.models import ResourceRequest
from sustainability.models import SustainabilityImpact
from transfers.models import Approval, Reservation, Transfer
from transfers.views import DECIDER_ACTIONS

from .helpers import DemoTestCase, FakeClaude

# The main pages and the actions that open them (the same action names the views check). None: every signed-in user.
PAGES = {
    "/": None, "/assets/": ("asset.view",), "/assets/search/": ("listing.search",),
    "/requests/": ("request.submit", "request.approve"), "/transfers/approvals/": DECIDER_ACTIONS,
    "/transfers/": ("transfer.view", "hold.confirm"), "/sustainability/": ("dashboard.view",),
    "/reports/": ("report.view",), "/history/audit-log/": ("audit.view",),
    "/accounts/administration/": ("role.authorise", "role.apply"),
}


def meaning(prompt):
    count = len(re.findall(r"^Item \d+:", prompt, re.M))
    return MeaningAnswer(items=[MeaningScore(item=i, similarity=0.9, reason="fits a seminar room")
                                for i in range(1, count + 1)])


@override_settings(ANTHROPIC_API_KEY="")  # no test in this file can reach the real AI
class SystemWorkflowTests(DemoTestCase):
    def setUp(self):
        self.aisha, self.omar, self.fatima = (self.sign_in(u) for u in ("comp.requester", "comp.rep", "comp.custodian"))
        self.khalid, self.mariam = self.sign_in("eng.custodian"), self.sign_in("eng.rep")

    def register(self, name, **extra):
        """Khalid saves a draft through the Register page."""
        data = {"kind": "general", "name": name, "description": "Spare item from a lab refresh", "condition": "good",
                "category": Category.objects.get(subcategory="Monitor").pk, "quantity": 2, "campus": "Main campus",
                "building": "Engineering Building", "room": "E2-114", "specifications": "24-inch, HDMI",
                "purchase_date": "2024-01-15", "value": "345"}
        data.update(extra)
        self.khalid.post("/assets/register/", data)
        return Asset.objects.get(name=name), data

    def publish(self, asset, quantity):
        """Khalid offers the asset and sends it for release; Mariam approves. Returns the listing."""
        self.khalid.post(f"/assets/{asset.pk}/list/", {"quantity": quantity, "available_from": date.today().isoformat(),
                                                       "release_reason": "surplus", "submit_for": "release"})
        listing = asset.listings.get()
        self.assertEqual(listing.status, Listing.Status.PENDING_RELEASE)
        self.mariam.post(f"/assets/listings/{listing.pk}/decide/", {"decision": "approve"})
        listing.refresh_from_db()
        return listing

    def decide(self, client, approval):
        return client.post(f"/transfers/approvals/{approval.pk}/", {"decision": "approve", "reason": ""}, follow=True)

    @staticmethod
    def actions(record):
        return list(AuditLog.for_record(record).values_list("action", flat=True))

    @staticmethod
    def told(username, text):
        return User.objects.get(username=username).notifications.filter(message__contains=text).exists()

    def test_asset_goes_from_registration_to_search(self):
        asset, _ = self.register("BenQ 24-inch monitor")
        self.assertEqual((asset.status, asset.owner_department.code, asset.custodian.username),
                         ("AS-01", "ENG", "eng.custodian"))
        self.assertIn("registered", self.actions(asset))
        # Khalid registered it, so he cannot confirm it himself (BR-02), and the refusal is logged.
        response = self.khalid.post(f"/assets/{asset.pk}/confirm/", {"placement": "in_storage"}, follow=True)
        asset.refresh_from_db()
        self.assertEqual(asset.status, "AS-01")
        self.assertTrue(any("BR-02" in e for e in self.errors(response)))
        self.assertIn("blocked: confirm asset", self.actions(asset))
        self.mariam.post(f"/assets/{asset.pk}/confirm/", {"placement": "in_storage"})
        asset.refresh_from_db()
        self.assertEqual((asset.status, asset.verified_by.username), ("AS-03", "eng.rep"))
        self.assertNotContains(self.aisha.get("/assets/search/?q=BenQ"), "BenQ 24-inch monitor")  # not published yet
        self.khalid.post(f"/assets/{asset.pk}/list/", {"quantity": 2, "available_from": date.today().isoformat(),
                                                       "release_reason": "surplus", "submit_for": "release"})
        listing = asset.listings.get()
        task = Approval.objects.get(listing=listing)
        self.assertEqual((listing.status, task.stage, task.status), ("LS-02", "listing_release", "AT-01"))
        self.assertTrue(self.told("eng.rep", "New approval task"))
        self.mariam.post(f"/assets/listings/{listing.pk}/decide/", {"decision": "approve"})
        listing.refresh_from_db()
        task.refresh_from_db()
        self.assertEqual((listing.status, task.status, task.approver.username), ("LS-03", "AT-02", "eng.rep"))
        self.assertTrue(self.told("eng.custodian", "is published and visible in search"))
        self.assertContains(self.aisha.get("/assets/search/?q=BenQ"), "BenQ 24-inch monitor")

    def test_request_to_completed_transfer(self):
        self.aisha.post("/requests/new/", {
            "purpose": "Monitors for the tutorial room", "category": Category.objects.get(subcategory="Monitor").pk,
            "quantity": 2, "min_condition": "fair", "urgency": "normal", "required_by": self.future(),
            "submit_for": "approval", "specifications": "24-inch, HDMI", "delivery_location": "Computing Building C1-105"})
        request = ResourceRequest.objects.get(purpose="Monitors for the tutorial room")
        self.assertEqual(request.status, "RQ-02")
        self.assertTrue(self.told("comp.rep", "New approval task"))
        self.decide(self.omar, request.approvals.get())
        request.refresh_from_db()
        self.assertEqual(request.status, "RQ-03")
        self.assertTrue(self.told("comp.requester", f"Your request {request.code} was approved"))

        listing = Listing.objects.get(asset__name__startswith="Dell", asset__owner_department__code="ENG", status="LS-03")
        asset = listing.asset
        self.assertEqual((asset.quantity, asset.available_qty, asset.reserved_qty, asset.allocated_qty), (2, 2, 0, 0))
        self.aisha.post("/transfers/holds/request/", {"request": request.pk, "listing": listing.pk})
        hold = Reservation.objects.get(request=request)
        request.refresh_from_db()
        asset.refresh_from_db()
        self.assertEqual((hold.status, request.status, asset.available_qty), ("RV-01", "RQ-04", 2))  # nothing held yet
        self.khalid.post(f"/transfers/holds/{hold.pk}/decide/", {"decision": "confirm"})
        hold.refresh_from_db()
        asset.refresh_from_db()
        self.assertEqual((hold.status, asset.available_qty, asset.reserved_qty), ("RV-02", 0, 2))
        self.aisha.post(f"/transfers/holds/{hold.pk}/start/", {
            "to_custodian": User.objects.get(username="comp.custodian").pk, "to_building": "Computing Building",
            "delivery_arrangement": "delivery", "distance_km": "10", "van_trips": "1", "transfer_cost_aed": "40",
            "planned_date": date.today().isoformat()})
        transfer = Transfer.objects.get(reservation=hold)
        hold.refresh_from_db()
        request.refresh_from_db()
        asset.refresh_from_db()
        self.assertEqual((transfer.status, hold.status, request.status), ("TR-01", "RV-04", "RQ-05"))
        self.assertEqual((asset.reserved_qty, asset.allocated_qty), (0, 2))
        self.decide(self.mariam, transfer.approvals.get(status="AT-01"))
        transfer.refresh_from_db()
        self.assertEqual(transfer.status, "TR-02")
        self.decide(self.omar, transfer.approvals.get(status="AT-01"))
        transfer.refresh_from_db()
        self.assertEqual(transfer.status, "TR-04")  # AED 690 is below the finance threshold, so no policy stage
        self.khalid.post(f"/transfers/{transfer.pk}/hand-over/", {"condition": asset.condition})
        transfer.refresh_from_db()
        asset.refresh_from_db()
        self.assertEqual((transfer.status, asset.owner_department.code), ("TR-05", "ENG"))  # still Engineering's
        self.fatima.post(f"/transfers/{transfer.pk}/receive/", {"received_quantity": 2, "outcome": "ok",
                                                                "received_condition": asset.condition})
        transfer.refresh_from_db()
        request.refresh_from_db()
        received = transfer.received_asset
        self.assertEqual((transfer.status, request.status), ("TR-06", "RQ-06"))
        self.assertEqual((received.owner_department.code, received.custodian.username), ("COMP", "comp.custodian"))
        self.assertEqual(SustainabilityImpact.objects.filter(transfer=transfer).count(), 1)
        history = self.fatima.get(f"/history/asset/{received.pk}/").content.decode()
        for step in ("Hold confirmed", "Transfer created", "Handed over", "Receipt confirmed"):
            self.assertIn(step, history)
        self.assertTrue(self.told("comp.requester", "was received by Computing"))

    @override_settings(ANTHROPIC_API_KEY="test-key")
    def test_ai_assisted_path_with_a_person_deciding_each_time(self):
        fake = FakeClaude({
            ClassificationAnswer: lambda p: ClassificationAnswer(category="IT equipment / Monitor", condition="good",
                                                                 tags=["monitor"], reason="It is a monitor.",
                                                                 missing_details=[]),
            MeaningAnswer: meaning, ReportAnswer: lambda p: ReportAnswer(summary="2 items were reused.")})
        asset, _ = self.register("Samsung 27-inch monitor", category="", condition="fair", quantity=1)
        salem = self.sign_in("sustainability.officer")
        with mock.patch("ai.adapter.anthropic.Anthropic", return_value=fake):
            # AI 1: the suggestion is saved, but the asset changes only when Khalid accepts it.
            self.khalid.post(f"/ai/assets/{asset.pk}/classify/")
            suggestion = AiSuggestion.objects.get(asset=asset)
            asset.refresh_from_db()
            self.assertEqual((fake.calls, float(suggestion.confidence), suggestion.user_response), (3, 1.0, "pending"))
            self.assertEqual((asset.category, asset.condition, asset.tags), (None, "fair", ""))
            self.khalid.post(f"/ai/suggestions/{suggestion.pk}/respond/", {"decision": "accept"})
            asset.refresh_from_db()
            suggestion.refresh_from_db()
            self.assertEqual((asset.category.subcategory, asset.condition, suggestion.user_response),
                             ("Monitor", "good", "accepted"))
            # AI 2: the matches are ranked; choosing the first one only asks for a hold.
            request = ResourceRequest.objects.get(purpose__startswith="Projector")
            self.aisha.post(f"/ai/requests/{request.pk}/matches/")
            top = MatchRecommendation.objects.filter(request=request).get(rank=1)
            self.assertEqual(top.score, sum(f["points"] for f in top.explanation["factors"]))
            self.aisha.post(f"/ai/matches/{top.pk}/choose/")
            request.refresh_from_db()
            projector = top.asset
            projector.refresh_from_db()
            self.assertEqual((request.status, Reservation.objects.get(request=request).status), ("RQ-04", "RV-01"))
            self.assertEqual((projector.available_qty, projector.reserved_qty), (1, 0))  # choosing alone holds nothing
            # AI 5: a number that is not in the figures stops the publishing; without it the summary is published.
            salem.post("/ai/report/draft/")
        draft = AiSuggestion.objects.get(task="report")
        refused = salem.post(f"/ai/report/{draft.pk}/publish/", follow=True, data={
            "summary": "2 items were reused. We also saved AED 9,999 on delivery.", "decision": "publish"})
        draft.refresh_from_db()
        self.assertEqual(draft.user_response, "pending")
        self.assertTrue(any("9,999" in e for e in self.errors(refused)))
        salem.post(f"/ai/report/{draft.pk}/publish/", {"summary": "2 items were reused.", "decision": "publish"})
        draft.refresh_from_db()
        self.assertEqual(draft.user_response, "accepted")
        self.assertContains(salem.get("/sustainability/"), "2 items were reused.")

    def test_everything_still_works_without_the_ai(self):
        self.assertFalse(ClaudeAdapter.is_configured())
        asset, data = self.register("Optoma portable projector", category="", quantity=1, value="900",
                                    specifications="3,000 lumens, HDMI")
        response = self.khalid.post(f"/ai/assets/{asset.pk}/classify/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose the category, condition and tags yourself")
        self.assertFalse(AiSuggestion.objects.exists())
        # The classic way: Khalid chooses the category by hand, Mariam confirms, and the item is published.
        self.khalid.post(f"/assets/{asset.pk}/edit/", {**data, "category": Category.objects.get(subcategory="Projector").pk})
        asset.refresh_from_db()
        self.assertEqual(asset.category.subcategory, "Projector")
        self.mariam.post(f"/assets/{asset.pk}/confirm/", {"placement": "in_storage"})
        listing = self.publish(asset, 1)
        self.assertEqual(listing.status, "LS-03")
        self.assertContains(self.aisha.get("/assets/search/?q=Optoma"), "Optoma portable projector")
        # The match page and AI search say the AI is not available and point to the normal way.
        request = ResourceRequest.objects.get(purpose__startswith="Projector")
        matches = self.aisha.post(f"/ai/requests/{request.pk}/matches/", follow=True)
        self.assertEqual(matches.status_code, 200)
        self.assertContains(matches, "classic order")
        self.assertTrue(all(m.score is None for m in MatchRecommendation.objects.filter(request=request)))
        self.assertContains(self.aisha.get("/assets/search/"), "AI search is not available right now")
        search = self.aisha.post("/ai/search/", {"query": "a projector"}, follow=True)
        self.assertEqual(search.status_code, 200)
        self.assertContains(search, "work without AI")
        # The hold is asked from the item's own page, with no AI involved.
        self.assertContains(self.aisha.get(f"/assets/listings/{listing.pk}/"), "Use this item")
        self.aisha.post("/transfers/holds/request/", {"request": request.pk, "listing": listing.pk})
        request.refresh_from_db()
        self.assertEqual((request.status, Reservation.objects.get(request=request, listing=listing).status),
                         ("RQ-04", "RV-01"))

    def test_every_role_reaches_only_its_own_pages(self):
        refused_before = AuditLog.objects.filter(action__startswith="blocked:", record_type="page").count()
        opened = refused = 0
        for user in User.objects.order_by("username"):
            client, role = self.sign_in(user.username), user.active_user_roles().first()
            for url, actions in PAGES.items():
                allowed = actions is None or any(role.allows(action) for action in actions)
                with self.subTest(user=user.username, role=str(role), url=url):
                    self.assertEqual(client.get(url).status_code, 200 if allowed else 403)
                opened, refused = opened + allowed, refused + (not allowed)
        self.assertEqual(opened + refused, 12 * len(PAGES))
        # Every refused page was written to the audit log.
        logged = AuditLog.objects.filter(action__startswith="blocked:", record_type="page").count() - refused_before
        self.assertEqual(logged, refused)
