"""AuditLog from the class diagram. Entries are insert-only (BR-17)."""

from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_entries"
    )
    role = models.CharField(max_length=60, blank=True)
    action = models.CharField(max_length=80)
    record_type = models.CharField(max_length=40)
    record_id = models.PositiveIntegerField()
    before_value = models.CharField(max_length=120, blank=True)
    after_value = models.CharField(max_length=120, blank=True)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [models.Index(fields=["record_type", "record_id"])]

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.record_type} {self.record_id}: {self.action}"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValueError("Audit entries cannot be changed. Add a new entry instead (BR-17).")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError("Audit entries cannot be deleted (BR-17).")

    @classmethod
    def record(cls, actor, action, obj, before="", after="", reason="", role=""):
        """Write one entry: who did what to which record, when, and why."""
        # The sign-in middleware puts the user's active role on the user object.
        role = role or str(getattr(actor, "active_role", "") or "")
        return cls.objects.create(
            user=actor if getattr(actor, "pk", None) else None,
            role=role,
            action=action,
            record_type=obj._meta.model_name,
            record_id=obj.pk,
            before_value=str(before or ""),
            after_value=str(after or ""),
            reason=reason or "",
        )

    @classmethod
    def for_record(cls, obj):
        return cls.objects.filter(record_type=obj._meta.model_name, record_id=obj.pk).select_related("user")
