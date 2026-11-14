"""Notification from the class diagram (in-app messages, FR-16)."""

from django.conf import settings
from django.db import models
from django.utils import timezone


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    record_type = models.CharField(max_length=40)
    record_id = models.PositiveIntegerField()
    message = models.CharField(max_length=255)
    # Added in Phase 6: where the notification links to (FR-16.4).
    link = models.CharField(max_length=200, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-sent_at", "-id"]

    def __str__(self):
        return self.message

    @property
    def is_read(self):
        return self.read_at is not None

    def mark_read(self):
        if self.read_at is None:
            self.read_at = timezone.now()
            self.save(update_fields=["read_at"])

    @classmethod
    def send(cls, users, record, message, link=""):
        """Create one message per user, skipping duplicates and empty users."""
        seen = set()
        created = []
        for user in users:
            if user is None or user.pk in seen:
                continue
            seen.add(user.pk)
            created.append(cls.objects.create(
                user=user, record_type=record._meta.model_name, record_id=record.pk, message=message[:255], link=link,
            ))
        return created
