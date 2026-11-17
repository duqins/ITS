"""AI features 1, 2 and 5 with a stand-in for Claude, plus the fallback when no key is set."""

import re
from unittest import mock

from django.test import override_settings

from ai.adapter import ClaudeAdapter
from ai.classification import ClassificationAnswer, ClassificationService
from ai.matching import MatchingService, MeaningAnswer, MeaningScore
from ai.models import AiSuggestion, MatchRecommendation
from ai.report_drafts import ReportAnswer, unsupported_numbers
from assets.models import Asset, Category
from resource_requests.models import ResourceRequest

from .helpers import DemoTestCase, FakeClaude


def classification(category):
    return lambda prompt: ClassificationAnswer(category=category, condition="good", tags=["monitor", "display"],
                                               reason="It is a monitor.", missing_details=[])


def meaning(prompt):
    count = len(re.findall(r"^Item \d+:", prompt, re.M))
    return MeaningAnswer(items=[MeaningScore(item=i, similarity=0.9, reason="fits a seminar room")
                                for i in range(1, count + 1)])


@override_settings(ANTHROPIC_API_KEY="test-key")
class ClassificationTests(DemoTestCase):
    def draft(self):
        custodian = self.sign_in("eng.custodian")
        custodian.post("/assets/register/", {"kind": "general", "name": "Samsung 27-inch monitor",
                                             "description": "Light scratches", "condition": "fair", "quantity": 1,
                                             "campus": "Main campus"})
        return custodian, Asset.objects.get(name="Samsung 27-inch monitor")

    def test_suggestion_with_confidence_and_human_accept(self):
        custodian, asset = self.draft()
        fake = FakeClaude({ClassificationAnswer: classification("IT equipment / Monitor")})
        with mock.patch("ai.adapter.anthropic.Anthropic", return_value=fake):
            custodian.post(f"/ai/assets/{asset.pk}/classify/")
        suggestion = AiSuggestion.objects.get(asset=asset)
        self.assertEqual(fake.calls, 3)
        self.assertEqual(float(suggestion.confidence), 1.0)
        asset.refresh_from_db()
        self.assertIsNone(asset.category)  # nothing changes before the custodian decides
        custodian.post(f"/ai/suggestions/{suggestion.pk}/respond/", {"decision": "accept"})
        asset.refresh_from_db()
        self.assertEqual(asset.category.subcategory, "Monitor")

    def test_below_060_is_an_option_only(self):
        custodian, asset = self.draft()
        answers = iter(["IT equipment / Monitor", "IT equipment / Laptop", "IT equipment / Projector"])
        fake = FakeClaude({ClassificationAnswer: lambda p: classification(next(answers))(p)})
        with mock.patch("ai.adapter.anthropic.Anthropic", return_value=fake):
            suggestion = ClassificationService().suggest(asset, asset.registered_by)
        self.assertLess(suggestion.confidence, 0.6)
        self.assertFalse(ClassificationService.can_prefill(suggestion))
        custodian.post(f"/ai/suggestions/{suggestion.pk}/respond/", {"decision": "accept"})
        asset.refresh_from_db()
        self.assertIsNone(asset.category)

    def test_claude_can_only_pick_an_allowed_category_and_answers_at_low_effort(self):
        _, asset = self.draft()
        fake = FakeClaude({ClassificationAnswer: classification("IT equipment / Monitor")})
        with mock.patch("ai.adapter.anthropic.Anthropic", return_value=fake):
            ClassificationService().suggest(asset, asset.registered_by)
        allowed = fake.output_format.model_json_schema()["properties"]["category"]["enum"]
        self.assertEqual(sorted(allowed), sorted(str(c) for c in Category.objects.filter(is_active=True)))
        self.assertEqual(fake.output_config, {"effort": "low"})


@override_settings(ANTHROPIC_API_KEY="test-key")
class MatchingTests(DemoTestCase):
    def test_top_matches_have_a_score_equal_to_the_factor_total(self):
        request = ResourceRequest.objects.get(purpose__startswith="Projector")
        with mock.patch("ai.adapter.anthropic.Anthropic", return_value=FakeClaude({MeaningAnswer: meaning})):
            matches, ai_used, _ = MatchingService().find(request)
        self.assertTrue(ai_used)
        self.assertLessEqual(len(matches), 5)
        top = matches[0]
        self.assertEqual(top.score, sum(f["points"] for f in top.explanation["factors"]))
        self.assertEqual(len(top.explanation["factors"]), 7)
        self.assertIsNone(top.confidence)
        self.assertTrue(top.reason)

    def test_choosing_a_lower_ranked_item_needs_a_reason(self):
        requester = self.sign_in("comp.requester")
        request = ResourceRequest.objects.get(purpose__startswith="Projector")
        match = MatchRecommendation.objects.create(request=request, asset=Asset.objects.get(name__startswith="Epson"),
                                                   listing=Asset.objects.get(name__startswith="Epson").listings.get(),
                                                   rank=2, score=60, explanation={"run": "x", "factors": []})
        requester.post(f"/ai/matches/{match.pk}/choose/")
        request.refresh_from_db()
        self.assertEqual(request.status, ResourceRequest.Status.OPEN)
        requester.post(f"/ai/matches/{match.pk}/choose/", {"reason": "Nearer to our room"})
        request.refresh_from_db()
        match.refresh_from_db()
        self.assertEqual(request.status, ResourceRequest.Status.RESERVATION_REQUESTED)
        self.assertEqual(match.user_response, "overridden")


class ReportDraftTests(DemoTestCase):
    def test_numbers_not_in_the_figures_are_caught(self):
        figures = "Items reused: 2\nAvoided purchase value (AED): 690"
        self.assertEqual(unsupported_numbers("2 items were reused, saving AED 690.", figures), [])
        self.assertEqual(unsupported_numbers("2 items were reused, saving AED 999.", figures), ["999"])

    @override_settings(ANTHROPIC_API_KEY="test-key")
    def test_draft_is_edited_and_published_by_a_reviewer(self):
        officer = self.sign_in("sustainability.officer")
        fake = FakeClaude({ReportAnswer: lambda p: ReportAnswer(summary="2 items were reused, avoiding 5 purchases.")})
        with mock.patch("ai.adapter.anthropic.Anthropic", return_value=fake):
            officer.post("/ai/report/draft/")
        draft = AiSuggestion.objects.get(task="report")
        officer.post(f"/ai/report/{draft.pk}/publish/", {"summary": draft.suggestion["summary"], "decision": "publish"})
        draft.refresh_from_db()
        self.assertEqual(draft.user_response, "pending")  # 5 purchases is not a database figure
        officer.post(f"/ai/report/{draft.pk}/publish/", {"summary": "2 items were reused.", "decision": "publish"})
        draft.refresh_from_db()
        self.assertEqual(draft.user_response, "corrected")
        self.assertContains(officer.get("/sustainability/"), "2 items were reused.")


@override_settings(ANTHROPIC_API_KEY="")
class NoKeyTests(DemoTestCase):
    def test_classic_path_without_ai(self):
        self.assertFalse(ClaudeAdapter.is_configured())
        request = ResourceRequest.objects.get(purpose__startswith="Projector")
        matches, ai_used, note = MatchingService().find(request)
        self.assertFalse(ai_used)
        self.assertTrue(matches and matches[0].score is None)
        self.assertIn("classic order", note)
        asset = Asset.objects.filter(status=Asset.Status.IN_STORAGE).first()
        self.assertContains(self.sign_in("eng.custodian").get(f"/assets/{asset.pk}/"), "AI unavailable")


@override_settings(ANTHROPIC_API_KEY="test-key")
class ReviewFixTests(DemoTestCase):
    def test_a_rejected_suggestion_cannot_be_applied_later(self):
        custodian = self.sign_in("eng.custodian")
        custodian.post("/assets/register/", {"kind": "general", "name": "Old screen", "condition": "fair",
                                             "quantity": 1, "campus": "Main campus"})
        asset = Asset.objects.get(name="Old screen")
        fake = FakeClaude({ClassificationAnswer: classification("IT equipment / Monitor")})
        with mock.patch("ai.adapter.anthropic.Anthropic", return_value=fake):
            custodian.post(f"/ai/assets/{asset.pk}/classify/")
        suggestion = AiSuggestion.objects.get(asset=asset)
        custodian.post(f"/ai/suggestions/{suggestion.pk}/respond/", {"decision": "reject", "reason": "Wrong"})
        custodian.post(f"/ai/suggestions/{suggestion.pk}/respond/", {"decision": "accept"})
        asset.refresh_from_db()
        self.assertIsNone(asset.category)

    def test_figures_check_catches_years_words_and_signs(self):
        figures = ("Period: 01 Jan 2026 to 05 Nov 2026\nDepartment: All departments\nItems reused: 2\n"
                   "Net financial savings (AED): 650\nCarbon saved, low estimate (kg CO2e): 254")
        ok = "From 1 January to 5 November 2026, 2 items saved AED 650 and about 254 kg CO2e."
        self.assertEqual(unsupported_numbers(ok, figures), [])
        self.assertEqual(unsupported_numbers("We diverted 2050 kg.", figures), ["2050"])
        self.assertEqual(unsupported_numbers("Forty items were reused.", figures), ["Forty"])
        self.assertEqual(unsupported_numbers("Savings were -650 AED.", figures), ["-650"])

    def test_choosing_one_match_rejects_the_rest_and_a_match_can_be_rejected(self):
        requester = self.sign_in("comp.requester")
        request = ResourceRequest.objects.get(purpose__startswith="Projector")
        epson = Asset.objects.get(name__startswith="Epson")
        listing = epson.listings.get()
        first = MatchRecommendation.objects.create(request=request, asset=epson, listing=listing, rank=1, score=80,
                                                   explanation={"run": "r1", "factors": []})
        second = MatchRecommendation.objects.create(request=request, asset=epson, listing=listing, rank=2, score=70,
                                                    explanation={"run": "r1", "factors": []})
        requester.post(f"/ai/matches/{second.pk}/reject/", {"reason": "Too far"})
        second.refresh_from_db()
        self.assertEqual(second.user_response, "rejected")
        third = MatchRecommendation.objects.create(request=request, asset=epson, listing=listing, rank=3, score=60,
                                                   explanation={"run": "r1", "factors": []})
        requester.post(f"/ai/matches/{first.pk}/choose/")
        third.refresh_from_db()
        self.assertEqual(third.user_response, "rejected")

    def test_published_summary_only_shows_for_its_own_scope(self):
        officer = self.sign_in("sustainability.officer")
        fake = FakeClaude({ReportAnswer: lambda p: ReportAnswer(summary="2 items were reused.")})
        with mock.patch("ai.adapter.anthropic.Anthropic", return_value=fake):
            officer.post("/ai/report/draft/")
        draft = AiSuggestion.objects.get(task="report")
        officer.post(f"/ai/report/{draft.pk}/publish/", {"summary": "2 items were reused.", "decision": "publish"})
        self.assertContains(officer.get("/sustainability/"), "2 items were reused.")
        other = officer.get("/sustainability/?date_from=2025-01-01&date_to=2025-12-31")
        self.assertNotContains(other, "2 items were reused.")
