"""AI search, added after the TA review on 17 November: a request in the user's own words, ranked by Claude as
JSON with item IDs, only when the user clicks. The tests use a fake Claude, so they need no key or network."""

import json
import re
from unittest import mock

from django.test import override_settings

from ai.models import AiSuggestion, Task
from ai.search import AISearchService, SearchAnswer, SearchHit
from assets.models import Listing

from .helpers import DemoTestCase, FakeClaude


def published_ids(prompt):
    return [int(i) for i in re.findall(r"^ID (\d+):", prompt, re.M)]


class AISearchTests(DemoTestCase):
    with_history = True

    def run_search(self, answer, query="something to show slides in a seminar room", user="comp.requester"):
        """Search through the page with a fake Claude whose answer is built from the prompt it receives."""
        fake = FakeClaude({SearchAnswer: answer})
        self.fake = fake
        client = self.sign_in(user)
        with override_settings(ANTHROPIC_API_KEY="test"), mock.patch("ai.adapter.anthropic.Anthropic",
                                                                     return_value=fake):
            response = client.post("/ai/search/", {"query": query})
        return client, response

    def test_results_are_ranked_checked_and_saved_and_the_json_is_shown(self):
        projector = Listing.objects.get(asset__name__startswith="Epson")
        laptops = Listing.objects.get(asset__name__startswith="Lenovo")

        def answer(prompt):
            self.prompt = prompt
            return SearchAnswer(results=[
                SearchHit(id=laptops.pk, relevance=40, reason="Can run slides on a screen"),
                SearchHit(id=projector.pk, relevance=140, reason="A projector for slides"),  # clamped to 100
                SearchHit(id=999999, relevance=99, reason="An item the app never sent"),  # dropped
                SearchHit(id=laptops.pk, relevance=10, reason="Repeated"),  # dropped
            ])

        client, response = self.run_search(answer)
        result = AiSuggestion.objects.get(task=Task.SEARCH)
        self.assertRedirects(response, f"/ai/search/{result.pk}/")
        self.assertEqual([r["id"] for r in result.suggestion["results"]], [projector.pk, laptops.pk])
        self.assertEqual(result.suggestion["results"][0]["relevance"], 100)
        self.assertEqual(result.created_by.username, "comp.requester")
        self.assertIsNone(result.confidence)
        page = client.get(f"/ai/search/{result.pk}/").content.decode()
        self.assertLess(page.index("Epson classroom projector"), page.index("Lenovo ThinkPad T14 laptops"))
        self.assertIn("Show the AI answer (JSON)", page)
        shown = json.loads(re.search(r'<pre dir="ltr">(.*?)</pre>', page, re.S).group(1).replace("&quot;", '"'))
        self.assertEqual([r["id"] for r in shown["results"]], [projector.pk, laptops.pk])
        self.assertNotIn("999999", page)

    def test_only_published_items_with_units_are_sent_and_no_names_of_people_or_departments(self):
        def answer(prompt):
            self.prompt = prompt
            return SearchAnswer(results=[])

        self.run_search(answer)
        sent = published_ids(self.prompt)
        expected = [l.pk for l in Listing.objects.filter(status=Listing.Status.PUBLISHED) if l.remaining_quantity() > 0]
        self.assertEqual(sorted(sent), sorted(expected))
        for name in ("Khalid", "Mariam", "Fatima", "Aisha", "Omar", "Department:", "Engineering Building"):
            self.assertNotIn(name, self.prompt)
        self.assertIn("Request: something to show slides in a seminar room", self.prompt)

    def test_it_runs_only_on_a_click(self):
        client = self.sign_in("comp.requester")
        self.assertEqual(client.get("/ai/search/").status_code, 405)  # opening the address never calls the AI
        page = client.get("/assets/search/").content.decode()
        self.assertIn("Search with AI", page)
        self.assertFalse(AiSuggestion.objects.filter(task=Task.SEARCH).exists())

    def test_without_the_ai_the_normal_search_still_works(self):
        client = self.sign_in("comp.requester")
        with override_settings(ANTHROPIC_API_KEY=""):
            page = client.get("/assets/search/").content.decode()
            self.assertIn("AI search is not available right now", page)
            response = client.post("/ai/search/", {"query": "a projector"}, follow=True)
        self.assertIn("work without AI", response.content.decode())
        self.assertFalse(AiSuggestion.objects.filter(task=Task.SEARCH).exists())

    def test_a_too_short_request_is_refused_and_results_are_private(self):
        client = self.sign_in("comp.requester")
        response = client.post("/ai/search/", {"query": "a"}, follow=True)
        self.assertIn("Describe what you need in a few words", response.content.decode())
        self.run_search(lambda prompt: SearchAnswer(results=[]), user="comp.requester")
        result = AiSuggestion.objects.get(task=Task.SEARCH)
        self.assertEqual(self.sign_in("eng.custodian").get(f"/ai/search/{result.pk}/").status_code, 404)

    def test_arabic_users_get_reasons_in_arabic(self):
        client = self.sign_in("comp.requester")
        client.post("/accounts/settings/language/", {"language": "ar"})
        fake = FakeClaude({SearchAnswer: lambda prompt: SearchAnswer(results=[])})
        with override_settings(ANTHROPIC_API_KEY="test"), mock.patch("ai.adapter.anthropic.Anthropic",
                                                                     return_value=fake):
            client.post("/ai/search/", {"query": "جهاز عرض"})
        self.assertEqual(fake.calls, 1)
        self.assertIn("Arabic", fake.system)  # the reasons are written in Arabic (in_language)

    def test_the_service_keeps_at_most_eight_results(self):
        listings = AISearchService.candidates()
        fake = FakeClaude({SearchAnswer: lambda prompt: SearchAnswer(results=[
            SearchHit(id=l.pk, relevance=50, reason="fits") for l in listings])})
        with override_settings(ANTHROPIC_API_KEY="test"), mock.patch("ai.adapter.anthropic.Anthropic",
                                                                     return_value=fake):
            result = AISearchService().search("anything useful", listings[0].asset.registered_by)
        self.assertLessEqual(len(result.suggestion["results"]), 8)
        self.assertEqual(result.suggestion["items_sent"], len(listings))
