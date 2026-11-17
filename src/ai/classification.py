"""AI feature 1: classification and tagging (AI-01, design section 4).

Claude suggests the category, condition and tags from the asset's description and up to two of its photos
(AI-01.1). Supporting PDF documents are not sent; the panel says so (AI-01.2). The custodian
accepts, edits or rejects it. Confidence is the share of three independent runs that agree on
the category (the Claude API has no token probabilities); the 0.60 threshold of SRS Table 4.2
decides whether the suggestion may be applied in one click.
"""

import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from typing import Literal

from django.conf import settings
from django.utils.translation import gettext_lazy, ngettext
from pydantic import BaseModel, create_model

from assets.models import AssetFile, Category

from .adapter import in_language, AIUnavailable, ClaudeAdapter, Deadline
from .models import AiSuggestion, ModelVersion, Task

SYSTEM = (
    "You classify campus assets for a university reuse system. Use only the information given. "
    "Choose exactly one category from the allowed list, written exactly as listed. Judge the condition "
    "from the description and any photos: new, good, fair, poor or not_working. If a photo is unclear or does "
    "not show the item, say so in the missing details. Give 3 to 6 short lowercase search tags. Write a standard "
    "one-sentence description of the item that keeps every fact the user gave. List details that are missing "
    "for a reliable record. Never include names of people."
)
# Version 2 of the classification prompt reads photos as well (saved with every suggestion, AI-12).
PROMPT_VERSION = "prompt v2"
PHOTOS_SENT = 2


class ClassificationAnswer(BaseModel):
    category: str
    condition: Literal["new", "good", "fair", "poor", "not_working"]
    tags: list[str]
    reason: str
    missing_details: list[str]


def answer_format(category_names):
    """The answer structure with the category limited to the allowed list, so Claude can only return one of them."""
    return create_model("ClassificationAnswer", __base__=ClassificationAnswer,
                        category=(Literal[tuple(category_names)], ...), description=(str, ...))


class ClassificationService:
    def __init__(self, adapter=None):
        self.adapter = adapter or ClaudeAdapter()
        self.model = settings.AI["CLASSIFICATION_MODEL"]
        self.runs = settings.AI["CLASSIFICATION_RUNS"]

    def prompt(self, asset, categories):
        allowed = "\n".join(f"- {c}" for c in categories)
        return (f"Allowed categories:\n{allowed}\n\nAsset name: {asset.name}\n"
                f"Description: {asset.description or 'none'}\nSpecifications: {asset.specifications or 'none'}")

    def content(self, asset, categories):
        """The question as text, or as the photos followed by the text when the asset has photos."""
        text = self.prompt(asset, categories)
        photos = list(asset.files.filter(kind=AssetFile.Kind.PHOTO).order_by("pk").only("data")[:PHOTOS_SENT])
        if not photos:
            return text, 0
        blocks = [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                               "data": base64.b64encode(bytes(photo.data)).decode("ascii")}}
                  for photo in photos]
        text += f"\nPhotos of the asset: {len(photos)}, shown above."
        return blocks + [{"type": "text", "text": text}], len(photos)

    def suggest(self, asset, user):
        """Run the classification and save it as an AiSuggestion waiting for the custodian's decision."""
        categories = {str(c): c for c in Category.objects.filter(is_active=True)}
        deadline = Deadline()
        prompt, photos_read = self.content(asset, categories)
        system = in_language(SYSTEM)  # read here: the worker threads below have no active language
        output_format = answer_format(list(categories))

        def one_run(_):
            try:
                answer = self.adapter.ask(Task.CLASSIFICATION, self.model, system, prompt, output_format,
                                          deadline, max_tokens=1500)
            except AIUnavailable as error:
                return error
            # Lazy: this runs in a worker thread without the user's language; the page translates it.
            return answer if answer.category in categories else AIUnavailable(
                gettext_lazy("Unknown category in the answer."))

        with ThreadPoolExecutor(max_workers=self.runs) as pool:
            results = list(pool.map(one_run, range(self.runs)))
        answers = [r for r in results if isinstance(r, ClassificationAnswer)]
        if not answers:
            raise next((r for r in results if isinstance(r, AIUnavailable)), AIUnavailable(gettext_lazy("No answer.")))

        votes = Counter(a.category for a in answers)
        category, count = votes.most_common(1)[0]
        agreeing = [a for a in answers if a.category == category]
        condition = Counter(a.condition for a in agreeing).most_common(1)[0][0]
        best = agreeing[0]
        confidence = Decimal(count) / Decimal(self.runs)
        return AiSuggestion.objects.create(
            task=Task.CLASSIFICATION,
            model_version=ModelVersion.current(Task.CLASSIFICATION, self.model, PROMPT_VERSION),
            asset=asset,
            suggestion={
                "category_id": categories[category].pk,
                "category": category,
                "condition": condition,
                "tags": [t.strip().lower() for t in best.tags if t.strip()][:6],
                "missing_details": best.missing_details[:5],
                "runs": [a.category for a in answers],
                # AI-01.1: a standard description, applied only when the person accepts or edits it.
                "description": getattr(best, "description", "").strip()[:500],
                # AI-01.2: which inputs the AI did not read, so the person checks them.
                "photos_read": photos_read,
                "photos_total": asset.files.filter(kind=AssetFile.Kind.PHOTO).count(),
                "photos_not_read": list(asset.files.filter(kind=AssetFile.Kind.PHOTO).order_by("pk")
                                        .values_list("name", flat=True)[PHOTOS_SENT:]),
                "documents_not_read": list(asset.files.filter(kind=AssetFile.Kind.DOCUMENT)
                                           .values_list("name", flat=True)),
            },
            confidence=confidence.quantize(Decimal("0.001")),
            # Shown on the classification panel. Same English for one and many runs; the plural form is for Arabic.
            confidence_basis=ngettext("%(agreeing)s of %(runs)s runs agreed on the category",
                                      "%(agreeing)s of %(runs)s runs agreed on the category", self.runs) % {
                "agreeing": count, "runs": self.runs},
            explanation=best.reason,
            created_by=user,
        )

    @staticmethod
    def can_prefill(suggestion):
        """SRS Table 4.2: at or above 0.60 the value may be filled in; below it is an option only."""
        return suggestion.confidence is not None and suggestion.confidence >= Decimal(
            str(settings.AI["CLASSIFICATION_THRESHOLD"]))
