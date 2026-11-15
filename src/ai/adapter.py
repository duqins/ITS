"""The AI adapter (component diagram, design section 11).

Every AI call goes through ClaudeAdapter. It applies the one 15-second deadline of
AI-13.2, asks Claude for a fixed JSON structure (structured outputs), and turns every
failure (no key, timeout, rate limit, refusal, malformed answer) into AIUnavailable so
the page can show the classic alternative. It logs timing and outcome, never keys or
personal data.
"""

import logging
import time
import uuid

import anthropic
from django.conf import settings
from pydantic import ValidationError

logger = logging.getLogger("dawra.ai")

PROMPT_VERSION = "prompt v1"


class AIUnavailable(Exception):
    """The AI could not answer in time or correctly; use the classic path."""


class Deadline:
    """One time limit for the whole user request, shared by all its AI calls and retries."""

    def __init__(self, seconds=None):
        self.ends_at = time.monotonic() + (seconds or settings.AI["DEADLINE_SECONDS"])

    def remaining(self):
        return self.ends_at - time.monotonic()


class ClaudeAdapter:
    def __init__(self, client=None):
        self.client = client

    @staticmethod
    def is_configured():
        return bool(settings.ANTHROPIC_API_KEY)

    def _client(self):
        if self.client is None:
            if not self.is_configured():
                raise AIUnavailable("No AI key is set, so the AI service is switched off.")
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY, max_retries=0)
        return self.client

    def ask(self, task, model, system, prompt, output_format, deadline, max_tokens=2000):
        """Ask one question and return the validated answer (an output_format instance)."""
        correlation = uuid.uuid4().hex[:8]
        started = time.monotonic()
        remaining = deadline.remaining()
        outcome = "ok"
        try:
            if remaining < 1:
                raise AIUnavailable("The 15-second limit was reached.")
            # Haiku 5.5 and Sonnet 5.5 think before answering unless told otherwise, and thinking counts
            # toward max_tokens. Low effort keeps these short tasks well inside the 15-second limit.
            response = self._client().with_options(timeout=remaining).messages.parse(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": prompt}],
                output_format=output_format,
                output_config={"effort": "low"},
            )
            if response.stop_reason == "refusal":
                raise AIUnavailable("The AI declined this request.")
            if response.stop_reason == "max_tokens" or response.parsed_output is None:
                raise AIUnavailable("The AI answer was incomplete.")
            return response.parsed_output
        except AIUnavailable as error:
            outcome = str(error)
            raise
        except anthropic.AuthenticationError:
            outcome = "authentication failed"
            raise AIUnavailable("The AI key was not accepted.")
        except anthropic.RateLimitError:
            outcome = "rate limited"
            raise AIUnavailable("The AI service is busy. Try again in a minute.")
        except anthropic.APITimeoutError:
            outcome = "timed out"
            raise AIUnavailable("The AI did not answer within 15 seconds.")
        except anthropic.APIConnectionError:
            outcome = "no connection"
            raise AIUnavailable("The AI service could not be reached.")
        except anthropic.APIStatusError as error:
            outcome = f"provider error {error.status_code}"
            raise AIUnavailable("The AI service returned an error.")
        except anthropic.APIError:  # any other client error, for example an unreadable response
            outcome = "client error"
            raise AIUnavailable("The AI service returned an answer the app could not read.")
        except (ValidationError, ValueError):
            outcome = "malformed answer"
            raise AIUnavailable("The AI answer did not have the expected structure.")
        finally:
            logger.info("ai task=%s id=%s model=%s duration=%.2fs outcome=%s",
                        task, correlation, model, time.monotonic() - started, outcome)
