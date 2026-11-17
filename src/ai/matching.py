"""AI feature 2: matching and ranking (AI-02 to AI-05, design sections 4 and 11).

1. EligibilityChecker (classic, no AI) keeps only items that pass the mandatory checks (BR-14).
2. SemanticMatcher asks Claude how close each item is in meaning to the request (0 to 1).
   This replaces the embeddings of the design, because the Claude API has no embedding model.
3. RankingModel is plain Django arithmetic with the fixed SRS Table 4.1 weights. Claude never
   sets the score. Missing values earn 0 points and are labelled "unknown".
4. MatchingService saves the top 5 as MatchRecommendation rows. If the AI is unavailable the
   requester still gets the eligible items in classic order, without invented scores.
"""

import re
import uuid
from datetime import date

from django.conf import settings
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.translation import gettext as _, ngettext
from pydantic import BaseModel

from assets.models import Asset, Condition, Listing
from transfers.models import add_working_days

from .adapter import in_language, PROMPT_VERSION, AIUnavailable, ClaudeAdapter, Deadline
from .models import MatchRecommendation, ModelVersion, Task

MAX_CANDIDATES = 20


class EligibilityChecker:
    """Mandatory checks before any ranking: published, available, enough units, condition, category, date."""

    def eligible(self, request):
        candidates = []
        listings = Listing.objects.filter(status=Listing.Status.PUBLISHED, asset__category=request.category,
                                          asset__status__in=Asset.ACTIVE).exclude(
            asset__owner_department=request.department).select_related("asset__category")
        for listing in listings:
            if listing.remaining_quantity() < request.quantity:
                continue
            if request.listing_problem(listing) is not None:  # minimum condition and date (BR-14)
                continue
            candidates.append(listing)
        # Classic order: available sooner first, then better condition.
        candidates.sort(key=lambda l: (l.available_from, -Condition.rank(l.asset.condition)))
        return candidates[:MAX_CANDIDATES]


class MeaningScore(BaseModel):
    item: int
    similarity: float
    reason: str


class MeaningAnswer(BaseModel):
    items: list[MeaningScore]


SYSTEM = (
    "You compare a campus resource request with surplus items. For each item, rate how well its kind and "
    "purpose fit the request, from 0 (unrelated) to 1 (exactly what is needed), and give a reason of at most "
    "12 words. Condition, quantity, location and dates are scored separately by fixed rules, so ignore them "
    "and do not mention them. Use only the text given. Return every item number exactly once."
)


class SemanticMatcher:
    def __init__(self, adapter=None):
        self.adapter = adapter or ClaudeAdapter()
        self.model = settings.AI["MATCHING_MODEL"]

    def similarities(self, request, listings, deadline):
        # Personal and department names are left out of the matching text (section 11).
        lines = [f"Item {i}: {l.asset.name}. {l.asset.description} Specifications: {l.asset.specifications or 'none'}. "
                 f"Tags: {l.asset.tags or 'none'}." for i, l in enumerate(listings, start=1)]
        prompt = (f"Request: {request.purpose}. Specifications: {request.specifications or 'none'}. "
                  f"Description: {request.description or 'none'}. "
                  f"Quantity: {request.quantity}.\n\nItems:\n" + "\n".join(lines))
        answer = self.adapter.ask(Task.MATCHING, self.model, in_language(SYSTEM), prompt, MeaningAnswer, deadline, max_tokens=2000)
        result = {}
        for score in answer.items:
            if 1 <= score.item <= len(listings) and score.item not in result:
                result[score.item] = (min(max(score.similarity, 0.0), 1.0), score.reason.strip())
        if len(result) != len(listings):
            raise AIUnavailable(_("The AI did not rate every item."))
        return {listings[i - 1].pk: value for i, value in result.items()}


class RankingModel:
    """SRS Table 4.1 (design Table 11.2): seven factors, 100 points in total."""

    def factor(self, name, points, maximum, used, unknown=False):
        return {"factor": name, "points": points, "max": maximum, "used": used, "unknown": unknown}

    def spec_items(self, text):
        return [p.strip().lower() for p in re.split(r"[,;\n]", text or "") if p.strip()]

    def score(self, request, listing, similarity):
        asset, today = listing.asset, timezone.localdate()
        # The factor texts are saved with the match and shown on the page, in the requester's language.
        factors = [self.factor(_("Meaning and purpose"), round(similarity * 30), 30,
                               _("Meaning match %(value)s (rated by the AI)") % {"value": f"{similarity:.2f}"})]

        wanted = self.spec_items(request.specifications)
        if wanted:
            haystack = f"{asset.name} {asset.description} {asset.specifications}".lower()
            met = sum(1 for item in wanted if all(word in haystack for word in item.split()))
            factors.append(self.factor(_("Technical fit"), round(20 * met / len(wanted)), 20,
                                       ngettext("%(met)s of %(wanted)s requested specifications met",
                                                "%(met)s of %(wanted)s requested specifications met", len(wanted))
                                       % {"met": met, "wanted": len(wanted)}))
        else:
            factors.append(self.factor(_("Technical fit"), 0, 20, _("No specifications requested"), unknown=True))

        above = Condition.rank(asset.condition) - Condition.rank(request.min_condition)
        factors.append(self.factor(_("Condition"), 15 if above >= 2 else 10 if above == 1 else 5, 15,
                                   _("%(condition)s against minimum %(minimum)s") % {
                                       "condition": asset.get_condition_display(),
                                       "minimum": request.get_min_condition_display()}))

        place = (request.delivery_location or "").lower()
        if not place:
            factors.append(self.factor(_("Location and transfer cost"), 0, 10, _("No delivery location given"),
                                       unknown=True))
        elif asset.building and asset.building.lower() in place:
            factors.append(self.factor(_("Location and transfer cost"), 10, 10, _("Same building")))
        elif asset.campus and asset.campus.lower() != "main campus" and asset.campus.lower() not in place:
            factors.append(self.factor(_("Location and transfer cost"), 2, 10,
                                       _("Other campus (%(campus)s)") % {"campus": asset.campus}))
        elif not asset.building:  # a missing value earns 0 and says so (SRS 4.1)
            factors.append(self.factor(_("Location and transfer cost"), 0, 10, _("Item building not recorded"),
                                       unknown=True))
        else:
            factors.append(self.factor(_("Location and transfer cost"), 6, 10,
                                       _("Other building (%(building)s)") % {"building": asset.building}))

        if listing.available_from <= today:
            availability = (10, _("Available now"))
        elif listing.available_from <= add_working_days(today, 5):
            availability = (6, _("Available from %(date)s") % {"date": date_format(listing.available_from)})
        else:
            availability = (2, _("Available from %(date)s, before the required date") % {
                "date": date_format(listing.available_from)})
        factors.append(self.factor(_("Availability"), availability[0], 10, availability[1]))

        if asset.planned_retirement_date:
            years = (asset.planned_retirement_date - today).days / 365
            points = 10 if years >= 3 else 6 if years >= 1 else 2
            factors.append(self.factor(_("Useful life left"), points, 10,
                                       _("About %(years)s years left") % {"years": f"{max(years, 0):.1f}"}))
        else:
            factors.append(self.factor(_("Useful life left"), 0, 10, _("Planned retirement date unknown"), unknown=True))

        if asset.condition in (Condition.NEW, Condition.GOOD):
            factors.append(self.factor(_("Repair cost"), 5, 5, _("No repair needed (condition New or Good)")))
        else:
            factors.append(self.factor(_("Repair cost"), 0, 5, _("No repair estimate recorded"), unknown=True))

        total = sum(f["points"] for f in factors)
        if not 0 <= total <= 100:  # the score always equals the factor total (section 11)
            raise ValueError(f"Score {total} is outside 0 to 100.")
        return total, factors


def short_reason(factors, ai_reason):
    """One line: the AI's meaning reason plus the strongest classic factors."""
    strong = [f["used"] for f in factors[1:] if not f["unknown"] and f["points"] == f["max"]][:2]
    return " · ".join([ai_reason.rstrip(".")] + strong)[:250]


def confidence_label(confidence):
    """SRS Table 4.2 for matching: 0.75 shown normally, 0.50 to 0.74 'Check carefully', below 0.50 withheld."""
    if confidence is None:
        return _("Confidence unavailable - check carefully")
    if confidence < settings.AI["MATCH_CHECK_CAREFULLY"]:
        return _("Withheld (confidence below 0.50)")
    if confidence < settings.AI["MATCH_SHOW_NORMALLY"]:
        return _("Confidence %(value)s - check carefully") % {"value": f"{confidence:.2f}"}
    return _("Confidence %(value)s") % {"value": f"{confidence:.2f}"}


class MatchingService:
    def __init__(self, adapter=None):
        self.checker = EligibilityChecker()
        self.matcher = SemanticMatcher(adapter)
        self.ranking = RankingModel()

    def find(self, request):
        """Returns (matches, ai_used, message)."""
        listings = self.checker.eligible(request)
        run = uuid.uuid4().hex[:12]
        shown = settings.AI["MATCHES_SHOWN"]
        if not listings:
            return [], False, _("No published item passes the mandatory checks (category, quantity, condition, date).")
        try:
            similarities = self.matcher.similarities(request, listings, Deadline())
        except AIUnavailable as error:
            matches = [MatchRecommendation.objects.create(
                request=request, asset=l.asset, listing=l, rank=i, score=None,
                reason=_("%(condition)s condition, available from %(date)s") % {
                    "condition": l.asset.get_condition_display(), "date": date_format(l.available_from)},
                explanation={"run": run, "classic": True, "factors": []},
            ) for i, l in enumerate(listings[:shown], start=1)]
            return matches, False, _("%(error)s Showing eligible items in classic order without AI scores.") % {
                "error": error}

        version = ModelVersion.current(Task.MATCHING, self.matcher.model, PROMPT_VERSION)
        scored = []
        for listing in listings:
            similarity, ai_reason = similarities[listing.pk]
            total, factors = self.ranking.score(request, listing, similarity)
            scored.append((total, listing, factors, ai_reason))
        # Ties go to earlier availability, then the nearer building (SRS 4.1).
        scored.sort(key=lambda s: (-s[0], s[1].available_from, -s[2][3]["points"]))
        matches = [MatchRecommendation.objects.create(
            request=request, asset=listing.asset, listing=listing, model_version=version, rank=i, score=total,
            confidence=None, reason=short_reason(factors, ai_reason),
            explanation={"run": run, "classic": False, "factors": factors, "ai_reason": ai_reason,
                         "confidence_basis": "No supported confidence measure for meaning ratings"},
        ) for i, (total, listing, factors, ai_reason) in enumerate(scored[:shown], start=1)]
        return matches, True, ""

    @staticmethod
    def latest(request):
        newest = request.matches.order_by("-created_at", "rank").first()
        if newest is None:
            return []
        return list(request.matches.filter(explanation__run=newest.explanation.get("run")).order_by("rank")
                    .select_related("asset__category", "asset__owner_department", "listing"))
