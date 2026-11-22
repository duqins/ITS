"""AI search, added after the TA review on 17 November.

The user describes what they need in their own words. Claude Haiku reads the published items (each with its
ID) and answers in JSON: the IDs of the items that fit, best first, each with a relevance from 0 to 100 and a
short reason. It extends search (FR-08) with the ideas of AI matching (AI-02 to AI-04):
- it runs only when the user clicks the button (a POST), never on page load;
- the app checks every ID against the items it sent and drops unknown or repeated ones (Claude cannot invent
  an item), and keeps relevance between 0 and 100;
- no names of people or departments are sent, only the item details;
- the 15-second limit applies, and if the AI fails the normal search still works;
- every answer is saved as an AiSuggestion (AI-12), and it only suggests: nothing is held or changed.
"""

from django.conf import settings
from django.utils.translation import gettext as _
from pydantic import BaseModel

from assets.models import Asset, Listing

from .adapter import PROMPT_VERSION, AIUnavailable, ClaudeAdapter, Deadline, in_language
from .models import AiSuggestion, ModelVersion, Task

MAX_ITEMS = 40     # items sent to the AI
MAX_RESULTS = 8    # items shown


class SearchHit(BaseModel):
    id: int
    relevance: int
    reason: str


class SearchAnswer(BaseModel):
    results: list[SearchHit]


SYSTEM = (
    "You help campus staff find surplus items they can reuse. You get a request in the user's own words and a "
    "list of published items, each with an ID. Return the items that fit the request, best first, at most 8. For "
    "each give its ID exactly as listed, a relevance from 0 (unrelated) to 100 (exactly what is needed) and a "
    "reason of at most 15 words. Leave out items that do not fit. Use only the text given."
)


class AISearchService:
    def __init__(self, adapter=None):
        self.adapter = adapter or ClaudeAdapter()
        self.model = settings.AI["MATCHING_MODEL"]

    @staticmethod
    def candidates():
        """Published items that still have units left, newest first."""
        listings = (Listing.objects.filter(status=Listing.Status.PUBLISHED, asset__status__in=Asset.ACTIVE)
                    .select_related("asset__category").order_by("-published_at", "-pk"))
        return [listing for listing in listings if listing.remaining_quantity() > 0][:MAX_ITEMS]

    @staticmethod
    def describe(listing):
        """One line per item: only what the item is, never who owns it."""
        asset = listing.asset
        return (f"ID {listing.pk}: {asset.name}. Category: {asset.category or 'not set'}. Condition: {asset.condition}. "
                f"{asset.description} Specifications: {asset.specifications or 'none'}. "
                f"Tags: {asset.tags or 'none'}. Units available: {listing.remaining_quantity()}.")

    def search(self, query, user):
        """Ask Claude to rank the published items for the query. Returns the saved AiSuggestion, or raises
        AIUnavailable (the page then points to the normal search)."""
        listings = self.candidates()
        if not listings:
            raise AIUnavailable(_("No items are published right now."))
        sent = {listing.pk for listing in listings}
        prompt = f"Request: {query}\n\nItems:\n" + "\n".join(self.describe(listing) for listing in listings)
        answer = self.adapter.ask(Task.SEARCH, self.model, in_language(SYSTEM), prompt, SearchAnswer, Deadline(),
                                  max_tokens=1500)
        results, seen = [], set()
        for hit in answer.results:
            if hit.id in sent and hit.id not in seen:  # an ID the app did not send is never shown
                seen.add(hit.id)
                results.append({"id": hit.id, "relevance": min(max(hit.relevance, 0), 100),
                                "reason": hit.reason.strip()[:200]})
        results.sort(key=lambda r: -r["relevance"])  # best first; equal scores keep the AI's order
        return AiSuggestion.objects.create(
            task=Task.SEARCH, model_version=ModelVersion.current(Task.SEARCH, self.model, PROMPT_VERSION),
            suggestion={"query": query, "results": results[:MAX_RESULTS], "items_sent": len(listings)},
            confidence=None, confidence_basis="No supported confidence measure for relevance ratings",
            explanation=f"Ranked by {self.model} from {len(listings)} published items.",  # stored in English
            created_by=user)
