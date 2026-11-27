"""Phase 7 tests of the AI failure conditions (AI-13, NFR-07).

Our Phase 1 plan lists five conditions: the service is unavailable, it times out, it is rate
limited, its answer is malformed, and the confidence is too low. In each one the adapter must
report "AI unavailable" instead of failing, and the page must offer the classic way. The low
confidence case is in test_ai.py (below_060_is_an_option_only).
"""

from types import SimpleNamespace
from unittest import mock

import anthropic
import httpx2

from ai.adapter import AIUnavailable, ClaudeAdapter, Deadline
from ai.matching import MeaningAnswer
from ai.models import Task
from assets.models import Asset

from .helpers import DemoTestCase

REQUEST = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")


class FailingClaude:
    """Stands in for the Anthropic client and fails in the way it is told to."""

    def __init__(self, failure):
        self.failure = failure
        self.messages = self
        self.timeout = None

    def with_options(self, timeout=None, **kwargs):
        self.timeout = timeout
        return self

    def parse(self, **kwargs):
        if isinstance(self.failure, Exception):
            raise self.failure
        return self.failure


FAILURES = {
    "timeout": anthropic.APITimeoutError(request=REQUEST),
    "rate limit": anthropic.RateLimitError("busy", response=httpx2.Response(429, request=REQUEST), body=None),
    "no connection": anthropic.APIConnectionError(request=REQUEST),
    "malformed answer": SimpleNamespace(stop_reason="end_turn", parsed_output=None),
    "answer cut short": SimpleNamespace(stop_reason="max_tokens", parsed_output=None),
    "refusal": SimpleNamespace(stop_reason="refusal", parsed_output=None),
}

# The message the user sees for each failure.
MESSAGES = {
    "timeout": "The AI did not answer within 15 seconds.",
    "rate limit": "The AI service is busy. Try again in a minute.",
    "no connection": "The AI service could not be reached.",
    "malformed answer": "The AI answer was incomplete.",
    "answer cut short": "The AI answer was incomplete.",
    "refusal": "The AI declined this request.",
}


class AIFailureTests(DemoTestCase):
    def test_every_failure_becomes_ai_unavailable(self):
        """ClaudeAdapter.ask: each kind of failure is turned into AIUnavailable with a message for the user."""
        for name, failure in FAILURES.items():
            with self.subTest(failure=name):
                client = FailingClaude(failure)
                with self.assertRaises(AIUnavailable) as raised:
                    ClaudeAdapter(client=client).ask(Task.MATCHING, "claude-haiku-5-5", "system", "prompt",
                                                     MeaningAnswer, Deadline())
                self.assertEqual(str(raised.exception), MESSAGES[name])
                self.assertTrue(0 < client.timeout <= 15)   # the call may never wait longer than the 15 seconds

    def test_no_key_and_spent_deadline(self):
        """ClaudeAdapter.ask: no API key, and a time limit that has already passed, also give AIUnavailable."""
        with self.settings(ANTHROPIC_API_KEY=""), self.assertRaises(AIUnavailable):
            ClaudeAdapter().ask(Task.MATCHING, "claude-haiku-5-5", "system", "prompt", MeaningAnswer, Deadline())
        with self.assertRaises(AIUnavailable) as raised:
            ClaudeAdapter(client=FailingClaude(None)).ask(Task.MATCHING, "claude-haiku-5-5", "system", "prompt",
                                                          MeaningAnswer, Deadline(seconds=0.5))
        self.assertEqual(str(raised.exception), "The 15-second limit was reached.")

    def test_a_timeout_on_the_page_keeps_the_draft_and_offers_the_classic_way(self):
        """Classify button during a timeout: no server error, nothing changed, and the user is told what to do."""
        client = self.sign_in("eng.custodian")
        client.post("/assets/register/", {"kind": "general", "name": "Spare screen", "condition": "fair",
                                          "quantity": 1, "campus": "Main campus"})
        asset = Asset.objects.get(name="Spare screen")
        failing = FailingClaude(FAILURES["timeout"])
        with self.settings(ANTHROPIC_API_KEY="test-key"), mock.patch("ai.adapter.anthropic.Anthropic",
                                                                     return_value=failing):
            response = client.post(f"/ai/assets/{asset.pk}/classify/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose the category, condition and tags yourself.")
        asset.refresh_from_db()
        self.assertIsNone(asset.category)
        self.assertEqual(asset.status, Asset.Status.DRAFT)
