"""ModelVersion, AiSuggestion and MatchRecommendation from the class diagram (AI logging, section 11)."""

from django.conf import settings
from django.db import models
from django.utils import timezone

from audit.models import AuditLog


class Task(models.TextChoices):
    CLASSIFICATION = "classification", "Classification"
    MATCHING = "matching", "Matching"
    ADVICE = "advice", "Advice"
    ASSISTANT = "assistant", "Assistant"
    REPORT = "report", "Report"


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
        PENDING = "pending", "Waiting for a decision"
        ACCEPTED = "accepted", "Accepted"
        CORRECTED = "corrected", "Corrected"
        REJECTED = "rejected", "Rejected"

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


class MatchRecommendation(models.Model):
    class Response(models.TextChoices):
        PENDING = "pending", "Waiting for a decision"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        OVERRIDDEN = "overridden", "Chosen over a higher-ranked item"

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

    def summarize(self):
        if self.is_classic:
            return f"{self.asset.code} · classic result · {self.reason}"
        return f"{self.asset.code} · score {self.score} · {self.reason}"
