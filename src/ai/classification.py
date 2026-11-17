"""AI feature 1: classification and tagging (AI-01, design section 4).

Claude suggests the category, condition and tags from the asset's description. The custodian
accepts, edits or rejects it. Confidence is the share of three independent runs that agree on
the category (the Claude API has no token probabilities); the 0.60 threshold of SRS Table 4.2
decides whether the suggestion may be applied in one click.
"""

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from typing import Literal

from django.conf import settings
from django.utils.translation import gettext_lazy, ngettext
from pydantic import BaseModel, create_model

from assets.models import Category

from .adapter import in_language, PROMPT_VERSION, AIUnavailable, ClaudeAdapter, Deadline
from .models import AiSuggestion, ModelVersion, Task

SYSTEM = (
    "You classify campus assets for a university reuse system. Use only the information given. "
    "Choose exactly one category from the allowed list, written exactly as listed. Judge the condition "
    "from the description only: new, good, fair, poor or not_working. Give 3 to 6 short lowercase search "
    "tags. List details that are missing for a reliable record. Never include names of people."
)


class ClassificationAnswer(BaseModel):
    category: str
    condition: Literal["new", "good", "fair", "poor", "not_working"]
    tags: list[str]
    reason: str
    missing_details: list[str]


def answer_format(category_names):
    """The answer structure with the category limited to the allowed list, so Claude can only return one of them."""
    return create_model("ClassificationAnswer", __base__=ClassificationAnswer,
                        category=(Literal[tuple(category_names)], ...))


class ClassificationService:
    def __init__(self, adapter=None):
        self.adapter = adapter or ClaudeAdapter()
        self.model = settings.AI["CLASSIFICATION_MODEL"]
        self.runs = settings.AI["CLASSIFICATION_RUNS"]

    def prompt(self, asset, categories):
        allowed = "\n".join(f"- {c}" for c in categories)
        return (f"Allowed categories:\n{allowed}\n\nAsset name: {asset.name}\n"
                f"Description: {asset.description or 'none'}\nSpecifications: {asset.specifications or 'none'}")

    def suggest(self, asset, user):
        """Run the classification and save it as an AiSuggestion waiting for the custodian's decision."""
        categories = {str(c): c for c in Category.objects.filter(is_active=True)}
        deadline = Deadline()
        prompt = self.prompt(asset, categories)
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
