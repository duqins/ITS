"""ResourceRequest and RequestSpecification from the class diagram."""

from datetime import date

from django.conf import settings
from django.db import models
from django.utils import timezone

from accounts.models import Department
from assets.models import Category, Condition
from audit.lifecycle import BusinessRuleError, change_state


class RequestSpecification(models.Model):
    """What is needed. A composition part of ResourceRequest, stored in the same table (section 10)."""

    class Urgency(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"

    specifications = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    min_condition = models.CharField(max_length=12, choices=Condition.choices, default=Condition.FAIR)
    urgency = models.CharField(max_length=8, choices=Urgency.choices, default=Urgency.NORMAL)

    class Meta:
        abstract = True


class ResourceRequest(RequestSpecification):
    class Status(models.TextChoices):
        DRAFT = "RQ-01", "Draft"
        PENDING_APPROVAL = "RQ-02", "Pending department approval"
        OPEN = "RQ-03", "Open"
        RESERVATION_REQUESTED = "RQ-04", "Reservation requested"
        IN_TRANSFER = "RQ-05", "In transfer"
        FULFILLED = "RQ-06", "Fulfilled"
        NO_SUITABLE_ITEM = "RQ-07", "No suitable item"
        REJECTED = "RQ-08", "Rejected"
        CANCELLED = "RQ-09", "Cancelled"
        EXPIRED = "RQ-10", "Expired"

    ACTIVE = (Status.OPEN, Status.RESERVATION_REQUESTED)
    FINAL = (Status.FULFILLED, Status.NO_SUITABLE_ITEM, Status.REJECTED, Status.CANCELLED, Status.EXPIRED)
    # Allowed moves from the request state diagram (Figure 10.3, SRS Table 4.4).
    TRANSITIONS = {
        Status.DRAFT: {Status.PENDING_APPROVAL},
        Status.PENDING_APPROVAL: {Status.OPEN, Status.DRAFT, Status.REJECTED},
        Status.OPEN: {Status.PENDING_APPROVAL, Status.RESERVATION_REQUESTED, Status.NO_SUITABLE_ITEM,
                      Status.EXPIRED, Status.CANCELLED},
        Status.RESERVATION_REQUESTED: {Status.OPEN, Status.IN_TRANSFER, Status.CANCELLED},
        Status.IN_TRANSFER: {Status.OPEN, Status.FULFILLED},
    }

    purpose = models.CharField(max_length=200, help_text="What the item is for")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="requests")
    delivery_location = models.CharField(max_length=120, blank=True)
    required_by = models.DateField()
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="resource_requests")
    # Added in Phase 6: the requester's department, so its representative can approve (BR-03).
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="resource_requests")
    status = models.CharField(max_length=5, choices=Status.choices, default=Status.DRAFT)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"REQ-{self.pk:04d} {self.purpose}" if self.pk else self.purpose

    @property
    def code(self):
        return f"REQ-{self.pk:04d}"

    @property
    def is_final(self):
        return self.status in self.FINAL

    def check_details(self):
        # FR-07.1: a positive whole quantity and a required-by date that has not passed.
        if self.quantity < 1:
            raise BusinessRuleError("The quantity must be a positive whole number.", self, "submit request")
        if self.required_by < date.today():
            raise BusinessRuleError("The required-by date must not be in the past.", self, "submit request")

    def submit(self, by):
        """Send the request to the requester's department representative (RQ-01 to RQ-02)."""
        from transfers.models import Approval

        self.check_details()
        self.submitted_at = timezone.now()
        change_state(self, self.Status.PENDING_APPROVAL, by, "submitted", extra_fields=("submitted_at",))
        Approval.open(Approval.Stage.REQUEST_DEPARTMENT, self, requested_by=self.requester,
                      department=self.department)

    def pending_approval(self):
        from transfers.models import Approval

        return self.approvals.filter(status=Approval.Status.PENDING).first()

    def approve(self, by):
        approval = self.pending_approval()
        if approval is None:
            raise BusinessRuleError("This request has no approval task.", self, "approve request")
        approval.approve(by)
        change_state(self, self.Status.OPEN, by, "approved")

    def request_changes(self, by, reason):
        approval = self.pending_approval()
        if approval is None:
            raise BusinessRuleError("This request has no approval task.", self, "request changes")
        approval.request_changes(by, reason)
        change_state(self, self.Status.DRAFT, by, "changes requested", reason)

    def reject(self, by, reason):
        approval = self.pending_approval()
        if approval is None:
            raise BusinessRuleError("This request has no approval task.", self, "reject request")
        approval.reject(by, reason)
        change_state(self, self.Status.REJECTED, by, "rejected", reason)

    def cancel(self, by, reason):
        """The requester cancels; any holds are released (BR-20, FR-07.6)."""
        from transfers.models import Reservation

        if not reason:
            raise BusinessRuleError("Give a reason for cancelling (BR-20).", self, "cancel request")
        change_state(self, self.Status.CANCELLED, by, "cancelled", reason)
        for reservation in self.reservations.filter(status__in=Reservation.OPEN):
            reservation.cancel(by, "Request cancelled")

    def close_no_suitable_item(self, by, reason):
        change_state(self, self.Status.NO_SUITABLE_ITEM, by, "closed: no suitable item", reason)

    def expire(self):
        from transfers.models import Reservation

        change_state(self, self.Status.EXPIRED, None, "expired", "Required-by date passed")
        for reservation in self.reservations.filter(status__in=Reservation.OPEN):
            reservation.expire()
