"""ModelVersion, AiSuggestion and MatchRecommendation from the class diagram (AI logging, section 11)."""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy

from audit.models import AuditLog


class Task(models.TextChoices):
    CLASSIFICATION = "classification", gettext_lazy("Classification")
    MATCHING = "matching", gettext_lazy("Matching")
    ADVICE = "advice", gettext_lazy("Advice")
    ASSISTANT = "assistant", gettext_lazy("Assistant")
    REPORT = "report", gettext_lazy("Report")
    SEARCH = "search", gettext_lazy("Search")  # AI search, added after the TA review (17 November)


class ModelVersion(models.Model):
    task = models.CharField(max_length=20, choices=Task.choices)
    model_name = models.CharField(max_length=60)
    version = models.CharField(max_length=40)
    active_from = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-active_from"]
        constraints = [models.UniqueConstraint(fields=["task", "model_name", "version"], name="unique_model_version")]

    def __str__(self):
        return f"{self.model_name} ({self.version})"

    @classmethod
    def current(cls, task, model_name, version):
        """A model or prompt change creates a new row (section 11)."""
        obj, _ = cls.objects.get_or_create(task=task, model_name=model_name, version=version)
        return obj


class AiSuggestion(models.Model):
    class Response(models.TextChoices):
        PENDING = "pending", gettext_lazy("Waiting for a decision")
        ACCEPTED = "accepted", gettext_lazy("Accepted")
        CORRECTED = "corrected", gettext_lazy("Corrected")
        REJECTED = "rejected", gettext_lazy("Rejected")

    task = models.CharField(max_length=20, choices=Task.choices)
    model_version = models.ForeignKey(ModelVersion, on_delete=models.PROTECT, related_name="suggestions")
    asset = models.ForeignKey("assets.Asset", on_delete=models.CASCADE, null=True, blank=True, related_name="ai_suggestions")
    suggestion = models.JSONField()
    # Stored as null when there is no supported measure; never as zero (section 4).
    confidence = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)
    confidence_basis = models.CharField(max_length=120, blank=True)
    explanation = models.TextField(blank=True)
    user_response = models.CharField(max_length=10, choices=Response.choices, default=Response.PENDING)
    corrected_value = models.JSONField(null=True, blank=True)
    response_reason = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    responded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_task_display()} suggestion {self.pk}"

    @property
    def final_value(self):
        return self.corrected_value if self.user_response == self.Response.CORRECTED else self.suggestion

    def _respond(self, by, response, value=None, reason=""):
        self.user_response = response
        self.corrected_value = value
        self.response_reason = reason
        self.responded_by = by
        self.responded_at = timezone.now()
        self.save(update_fields=["user_response", "corrected_value", "response_reason", "responded_by", "responded_at"])
        AuditLog.record(by, f"AI {self.task} suggestion {response}", self, reason=reason)

    def accept(self, by):
        self._respond(by, self.Response.ACCEPTED)

    def correct(self, by, value, reason=""):
        self._respond(by, self.Response.CORRECTED, value, reason)

    def reject(self, by, reason):
        self._respond(by, self.Response.REJECTED, reason=reason)

    def apply_to_asset(self, values, by):
        """Write the chosen category, condition and tags onto the draft asset (BR-15: a person decided)."""
        from assets.models import Asset, Category
        from audit.lifecycle import BusinessRuleError

        asset = self.asset
        if asset.status != Asset.Status.DRAFT:
            raise BusinessRuleError(_("The asset is already confirmed; AI values can no longer be applied."), asset,
                                    "apply AI suggestion")
        asset.category = Category.objects.get(pk=values["category_id"])
        asset.condition = values["condition"]
        asset.tags = ", ".join(values["tags"])
        if values.get("description"):
            asset.description = values["description"]
        asset.save(update_fields=["category", "condition", "tags", "description"])
        AuditLog.record(by, "AI suggestion applied", asset, after=f"{asset.category}, {asset.get_condition_display()}")

    def accept_and_apply(self, by):
        self.apply_to_asset(self.suggestion, by)
        self.accept(by)

    def correct_and_apply(self, by, values, reason=""):
        self.apply_to_asset(values, by)
        self.correct(by, values, reason)


class MatchRecommendation(models.Model):
    class Response(models.TextChoices):
        PENDING = "pending", gettext_lazy("Waiting for a decision")
        ACCEPTED = "accepted", gettext_lazy("Accepted")
        REJECTED = "rejected", gettext_lazy("Rejected")
        OVERRIDDEN = "overridden", gettext_lazy("Chosen over a higher-ranked item")

    request = models.ForeignKey("resource_requests.ResourceRequest", on_delete=models.CASCADE, related_name="matches")
    asset = models.ForeignKey("assets.Asset", on_delete=models.CASCADE, related_name="matches")
    # Added in Phase 6: the published listing the match came from, so a hold can be requested from it.
    listing = models.ForeignKey("assets.Listing", on_delete=models.CASCADE, related_name="matches")
    model_version = models.ForeignKey(ModelVersion, on_delete=models.PROTECT, null=True, blank=True, related_name="matches")
    rank = models.PositiveSmallIntegerField()
    score = models.PositiveSmallIntegerField(null=True, blank=True)  # 0-100; empty for a classic result
    confidence = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)
    reason = models.CharField(max_length=255, blank=True)
    explanation = models.JSONField(default=dict)
    user_response = models.CharField(max_length=10, choices=Response.choices, default=Response.PENDING)
    override_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["request", "rank"]

    def __str__(self):
        return f"Match {self.rank} for {self.request}"

    @property
    def is_classic(self):
        return self.score is None

    def accept(self):
        self.user_response = self.Response.ACCEPTED
        self.save(update_fields=["user_response"])

    def override(self, reason):
        self.user_response = self.Response.OVERRIDDEN
        self.override_reason = reason
        self.save(update_fields=["user_response", "override_reason"])

    def reject(self, reason=""):
        self.user_response = self.Response.REJECTED
        self.override_reason = reason
        self.save(update_fields=["user_response", "override_reason"])

    def choose(self, by, reason=""):
        """The requester picks this item. It only asks for a hold; the other items of the same search are set aside."""
        from audit.lifecycle import BusinessRuleError
        from transfers.models import Reservation

        overriding = self.rank > 1 and self.score is not None
        if overriding and not reason:
            raise BusinessRuleError(_("You chose a lower-ranked item. Give a reason for the override (AI-05.2)."),
                                    self.request, "choose match")
        self.override(reason) if overriding else self.accept()
        Reservation.request_hold(self.request, self.listing, by)
        others = self.request.matches.filter(explanation__run=self.explanation.get("run"),
                                             user_response=self.Response.PENDING).exclude(pk=self.pk)
        for other in others:
            other.reject("Another item was chosen")

    def summarize(self):
        if self.is_classic:
            return f"{self.asset.code} · classic result · {self.reason}"
        return f"{self.asset.code} · score {self.score} · {self.reason}"
