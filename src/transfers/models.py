"""Approval, Reservation and Transfer from the class diagram (C5)."""

from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone, translation
from django.utils.translation import gettext as _, gettext_lazy

from accounts.models import Department, Role
from assets.models import Asset, Condition, FurnitureAsset, ITAsset, Listing
from audit.lifecycle import BusinessRuleError, change_state
from audit.models import AuditLog
from resource_requests.models import ResourceRequest


def add_working_days(start, days):
    """Count forward working days (Monday to Friday; UAE weekend is Saturday and Sunday)."""
    current = start
    while days > 0:
        current += timedelta(days=1)
        if current.weekday() < 5:
            days -= 1
    return current


class Approval(models.Model):
    class Stage(models.TextChoices):
        REQUEST_DEPARTMENT = "request_department", gettext_lazy("Department approval of the request")
        LISTING_RELEASE = "listing_release", gettext_lazy("Release of the listing")
        TRANSFER_RELEASE = "transfer_release", gettext_lazy("Release approval")
        TRANSFER_RECEIPT = "transfer_receipt", gettext_lazy("Receipt approval")
        TRANSFER_FINANCE = "transfer_finance", gettext_lazy("Policy approval: Finance")
        TRANSFER_PROCUREMENT = "transfer_procurement", gettext_lazy("Policy approval: Procurement")

    class Status(models.TextChoices):
        PENDING = "AT-01", gettext_lazy("Pending")
        APPROVED = "AT-02", gettext_lazy("Approved")
        REJECTED = "AT-03", gettext_lazy("Rejected")
        CHANGES_REQUESTED = "AT-04", gettext_lazy("Changes requested")
        WITHDRAWN = "AT-05", gettext_lazy("Withdrawn")

    TRANSITIONS = {Status.PENDING: {Status.APPROVED, Status.REJECTED, Status.CHANGES_REQUESTED, Status.WITHDRAWN}}
    # Who decides each stage (SRS Table 5.2, design section 6).
    STAGE_ROLES = {
        Stage.REQUEST_DEPARTMENT: Role.Code.DEPARTMENT_REPRESENTATIVE,
        Stage.LISTING_RELEASE: Role.Code.DEPARTMENT_REPRESENTATIVE,
        Stage.TRANSFER_RELEASE: Role.Code.DEPARTMENT_REPRESENTATIVE,
        Stage.TRANSFER_RECEIPT: Role.Code.DEPARTMENT_REPRESENTATIVE,
        Stage.TRANSFER_FINANCE: Role.Code.FINANCE_OFFICER,
        Stage.TRANSFER_PROCUREMENT: Role.Code.PROCUREMENT_OFFICER,
    }

    stage = models.CharField(max_length=25, choices=Stage.choices)
    status = models.CharField(max_length=5, choices=Status.choices, default=Status.PENDING)
    # The department whose representative decides; empty for campus-wide Finance and Procurement stages.
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    # Added in Phase 6: who created the record, so self-approval can be refused (BR-02).
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="approval_decisions"
    )
    approver_role = models.CharField(max_length=60, blank=True)
    reason = models.TextField(blank=True)
    record_version = models.PositiveIntegerField()
    decided_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Exactly one owner record is set (section 8).
    request = models.ForeignKey(ResourceRequest, on_delete=models.CASCADE, null=True, blank=True, related_name="approvals")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name="approvals")
    transfer = models.ForeignKey("Transfer", on_delete=models.CASCADE, null=True, blank=True, related_name="approvals")

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(request__isnull=False, listing__isnull=True, transfer__isnull=True)
                    | Q(request__isnull=True, listing__isnull=False, transfer__isnull=True)
                    | Q(request__isnull=True, listing__isnull=True, transfer__isnull=False)
                ),
                name="approval_has_exactly_one_owner",
            )
        ]

    def __str__(self):
        return _("%(stage)s for %(record)s") % {"stage": self.get_stage_display(), "record": self.record}

    @property
    def record(self):
        return self.request or self.listing or self.transfer

    @property
    def required_role(self):
        return self.STAGE_ROLES[self.stage]

    @classmethod
    def open(cls, stage, record, requested_by, department=None):
        owner = {ResourceRequest: "request", Listing: "listing"}.get(type(record), "transfer")
        approval = cls.objects.create(
            stage=stage, department=department, requested_by=requested_by,
            record_version=record.version, **{owner: record},
        )
        AuditLog.record(requested_by, "approval task created", approval, after=cls.Stage(approval.stage).label)
        return approval

    def is_overdue(self):
        days = settings.DAWRA["OVERDUE_WORKING_DAYS"]
        return self.status == self.Status.PENDING and add_working_days(self.created_at, days) < timezone.now()

    def can_be_decided_by(self, user):
        return user.has_role(self.required_role, self.department) and user != self.requested_by

    def _check_decision(self, by, needs_reason=False, reason=""):
        # Re-read the task under a lock, so a double click cannot decide it twice.
        current = Approval.objects.select_for_update().filter(pk=self.pk).values_list("status", flat=True).first()
        if current != self.Status.PENDING:
            raise BusinessRuleError(_("This task was already decided."), self.record, "decide approval")
        if by == self.requested_by:
            raise BusinessRuleError(_("You cannot approve your own request or record (BR-02)."), self.record,
                                    "decide approval")
        if not by.has_role(self.required_role, self.department):
            role = Role.Code(self.required_role).label
            if self.department:
                message = _("Only the %(role)s of %(department)s can decide this stage.") % {
                    "role": role, "department": self.department}
            else:
                message = _("Only the %(role)s can decide this stage.") % {"role": role}
            raise BusinessRuleError(message, self.record, "decide approval")
        if self.record.version != self.record_version:
            raise BusinessRuleError(_("The record changed after this task was created. Reload it and decide again."),
                                    self.record, "decide approval")
        if needs_reason and not reason.strip():
            raise BusinessRuleError(_("Give a reason for this decision (BR-20)."), self.record, "decide approval")

    def _decide(self, by, to, action, reason=""):
        self.approver = by
        with translation.override(settings.LANGUAGE_CODE):  # saved in English, like the history
            self.approver_role = str(getattr(by, "active_role", "") or Role.Code(self.required_role).label)
        self.decided_at = timezone.now()
        self.reason = reason
        change_state(self, to, by, action, reason,
                     extra_fields=("approver", "approver_role", "decided_at", "reason"))

    def approve(self, by, reason=""):
        self._check_decision(by)
        self._decide(by, self.Status.APPROVED, "approved", reason)

    def reject(self, by, reason):
        self._check_decision(by, needs_reason=True, reason=reason)
        self._decide(by, self.Status.REJECTED, "rejected", reason)

    def request_changes(self, by, reason):
        self._check_decision(by, needs_reason=True, reason=reason)
        self._decide(by, self.Status.CHANGES_REQUESTED, "changes requested", reason)

    def withdraw(self, reason="Parent record cancelled"):
        change_state(self, self.Status.WITHDRAWN, None, "withdrawn", reason)


class Reservation(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "RV-01", gettext_lazy("Requested")
        CONFIRMED = "RV-02", gettext_lazy("Confirmed")
        DECLINED = "RV-03", gettext_lazy("Declined")
        CONVERTED = "RV-04", gettext_lazy("Converted to transfer")
        EXPIRED = "RV-05", gettext_lazy("Expired")
        CANCELLED = "RV-06", gettext_lazy("Cancelled")

    OPEN = (Status.REQUESTED, Status.CONFIRMED)
    TRANSITIONS = {
        Status.REQUESTED: {Status.CONFIRMED, Status.DECLINED, Status.CANCELLED},
        Status.CONFIRMED: {Status.CONVERTED, Status.CANCELLED, Status.EXPIRED},
    }

    request = models.ForeignKey(ResourceRequest, on_delete=models.PROTECT, related_name="reservations")
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="reservations")
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=5, choices=Status.choices, default=Status.REQUESTED)
    expires_at = models.DateTimeField(null=True, blank=True)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )
    decision_reason = models.TextField(blank=True)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"HLD-{self.pk:04d}" if self.pk else _("Hold")

    @property
    def code(self):
        return f"HLD-{self.pk:04d}"

    @classmethod
    def request_hold(cls, resource_request, listing, by):
        """The requester asks the releasing team to hold units (RQ-03 to RQ-04). Selection alone holds nothing."""
        if by != resource_request.requester:
            raise BusinessRuleError(_("Only the requester can ask for a hold."), resource_request, "request hold")
        if resource_request.status != ResourceRequest.Status.OPEN:
            raise BusinessRuleError(_("A hold can only be requested for an open request."), resource_request,
                                    "request hold")
        if listing.status != Listing.Status.PUBLISHED:
            raise BusinessRuleError(_("This item is no longer published."), resource_request, "request hold")
        if listing.asset.owner_department_id == resource_request.department_id:
            raise BusinessRuleError(_("This item already belongs to your department, so there is nothing to transfer."),
                                    resource_request, "request hold")
        if resource_request.quantity > listing.remaining_quantity():
            left = listing.remaining_quantity()
            raise BusinessRuleError(
                _("Nothing is left to hold on this listing.") if left == 0 else
                _("Only %(left)s of the units you need are left on this listing.") % {"left": left},
                resource_request, "request hold"
            )
        reservation = cls.objects.create(
            request=resource_request, listing=listing, quantity=resource_request.quantity, requested_by=by
        )
        AuditLog.record(by, "hold requested", reservation, after="RV-01 Requested")
        change_state(resource_request, ResourceRequest.Status.RESERVATION_REQUESTED, by, "hold requested")
        return reservation

    def check_releasing_side(self, by):
        if by == self.requested_by:
            raise BusinessRuleError(_("You cannot confirm your own hold (BR-02)."), self, "confirm hold")
        department = self.listing.asset.owner_department
        if not (by.has_role(Role.Code.ASSET_CUSTODIAN, department)
                or by.has_role(Role.Code.DEPARTMENT_REPRESENTATIVE, department)):
            raise BusinessRuleError(_("Only a custodian or representative of %(department)s can decide this hold.")
                                    % {"department": department}, self, "confirm hold")

    def confirm(self, by):
        """Hold the units for 5 working days (BR-12). Locks the asset row so the last unit goes to one person."""
        self.check_releasing_side(by)
        with transaction.atomic():
            # Lock the hold, the listing and the asset; re-read them so two clicks cannot both reserve.
            if Reservation.objects.select_for_update().get(pk=self.pk).status != self.Status.REQUESTED:
                raise BusinessRuleError(_("This hold was already decided."), self, "confirm hold")
            listing = Listing.objects.select_for_update().get(pk=self.listing_id)
            if listing.status not in (Listing.Status.PUBLISHED, Listing.Status.FULLY_RESERVED):
                raise BusinessRuleError(_("This listing is no longer published."), self, "confirm hold")
            if listing.held_quantity() + self.quantity > listing.quantity:
                left = max(listing.quantity - listing.held_quantity(), 0)
                raise BusinessRuleError(
                    _("Every unit of this listing is already held for someone else.") if left == 0 else
                    _("Only %(left)s of the %(total)s listed units are still free; this hold asks for %(asked)s.")
                    % {"left": left, "total": listing.quantity, "asked": self.quantity}, self, "confirm hold")
            asset = Asset.objects.select_for_update().get(pk=self.listing.asset_id)
            if not asset.verification_is_recent():
                raise BusinessRuleError(
                    _("The asset must be checked again before a hold (last check over 90 days ago, BR-16)."),
                    self, "confirm hold")
            asset.reserve(self.quantity)
            self.decided_by = by
            self.expires_at = add_working_days(timezone.now(), settings.DAWRA["HOLD_WORKING_DAYS"])
            change_state(self, self.Status.CONFIRMED, by, "hold confirmed", extra_fields=("decided_by", "expires_at"))
            self.listing.refresh_reserved_state(by)

    def decline(self, by, reason):
        self.check_releasing_side(by)
        if not reason.strip():
            raise BusinessRuleError(_("Give a reason for declining (BR-20)."), self, "decline hold")
        self.decided_by = by
        self.decision_reason = reason
        change_state(self, self.Status.DECLINED, by, "hold declined", reason, extra_fields=("decided_by", "decision_reason"))
        self._reopen_request(by, "hold ended")

    def cancel(self, by, reason):
        was_confirmed = self.status == self.Status.CONFIRMED
        change_state(self, self.Status.CANCELLED, by, "hold cancelled", reason)
        if was_confirmed:
            self._give_back(by)
        self._reopen_request(by, "hold ended")

    def expire(self):
        was_confirmed = self.status == self.Status.CONFIRMED
        change_state(self, self.Status.EXPIRED, None, "hold expired", "Hold period ended (BR-12)")
        if was_confirmed:
            self._give_back(None)
        self._reopen_request(None, "hold ended")

    def _give_back(self, by):
        asset = Asset.objects.select_for_update().get(pk=self.listing.asset_id)
        asset.release(self.quantity)
        self.listing.refresh_reserved_state(by)

    def _reopen_request(self, by, action):
        if self.request.status == ResourceRequest.Status.RESERVATION_REQUESTED:
            change_state(self.request, ResourceRequest.Status.OPEN, by, action)


class Transfer(models.Model):
    class Status(models.TextChoices):
        PENDING_RELEASE = "TR-01", gettext_lazy("Pending release approval")
        PENDING_RECEIPT = "TR-02", gettext_lazy("Pending receipt approval")
        PENDING_POLICY = "TR-03", gettext_lazy("Pending policy approval")
        APPROVED = "TR-04", gettext_lazy("Approved")
        HANDED_OVER = "TR-05", gettext_lazy("Handed over")
        COMPLETED = "TR-06", gettext_lazy("Completed")
        DISPUTED = "TR-07", gettext_lazy("Disputed")
        REJECTED = "TR-08", gettext_lazy("Rejected")
        CANCELLED = "TR-09", gettext_lazy("Cancelled")

    class Arrangement(models.TextChoices):
        COLLECTION = "collection", gettext_lazy("Collection")
        DELIVERY = "delivery", gettext_lazy("Delivery")

    WAITING = (Status.PENDING_RELEASE, Status.PENDING_RECEIPT, Status.PENDING_POLICY)
    FINAL = (Status.COMPLETED, Status.REJECTED, Status.CANCELLED)
    # Allowed moves from the transfer state diagram (Figure 10.4, SRS Table 4.6).
    TRANSITIONS = {
        Status.PENDING_RELEASE: {Status.PENDING_RECEIPT, Status.REJECTED, Status.CANCELLED},
        Status.PENDING_RECEIPT: {Status.PENDING_POLICY, Status.APPROVED, Status.REJECTED, Status.CANCELLED},
        Status.PENDING_POLICY: {Status.APPROVED, Status.REJECTED, Status.CANCELLED},
        Status.APPROVED: {Status.HANDED_OVER, Status.CANCELLED},
        Status.HANDED_OVER: {Status.COMPLETED, Status.DISPUTED},
        Status.DISPUTED: {Status.COMPLETED, Status.CANCELLED},
    }

    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name="transfers")
    request = models.ForeignKey(ResourceRequest, on_delete=models.PROTECT, related_name="transfers")
    reservation = models.OneToOneField(Reservation, on_delete=models.PROTECT, related_name="transfer")
    quantity = models.PositiveIntegerField()
    from_department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="released_transfers")
    to_department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="received_transfers")
    to_custodian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="incoming_transfers")
    to_campus = models.CharField(max_length=60, default="Main campus")
    to_building = models.CharField(max_length=60, blank=True)
    to_room = models.CharField(max_length=30, blank=True)
    planned_date = models.DateField(null=True, blank=True)
    delivery_arrangement = models.CharField(max_length=10, choices=Arrangement.choices, default=Arrangement.COLLECTION)
    transfer_cost_aed = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    van_trips = models.PositiveIntegerField(default=0)
    distance_km = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0"))
    status = models.CharField(max_length=5, choices=Status.choices, default=Status.PENDING_RELEASE)
    version = models.PositiveIntegerField(default=1)
    approver = models.ForeignKey(  # the final approver only; earlier stages are Approval rows
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    handed_over_at = models.DateTimeField(null=True, blank=True)
    handed_over_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    handover_condition = models.CharField(max_length=12, choices=Condition.choices, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+")
    received_quantity = models.PositiveIntegerField(null=True, blank=True)
    received_condition = models.CharField(max_length=12, choices=Condition.choices, blank=True)
    dispute_note = models.TextField(blank=True)
    # When only some units move, the receiving department gets a new asset record.
    received_asset = models.ForeignKey(Asset, on_delete=models.PROTECT, null=True, blank=True, related_name="+")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"TRF-{self.pk:04d}" if self.pk else _("Transfer")

    @property
    def code(self):
        return f"TRF-{self.pk:04d}"

    @property
    def to_location(self):
        return ", ".join(p for p in (self.to_room, self.to_building, self.to_campus) if p)

    @property
    def value_aed(self):
        return (self.asset.value or Decimal("0")) * self.quantity

    def needs_finance(self):
        # BR-06: Finance approves when the value is at or above TBD-1.
        return self.value_aed >= Decimal(str(settings.DAWRA["FINANCE_APPROVAL_THRESHOLD_AED"]))

    def needs_procurement(self):
        return bool(self.asset.category and self.asset.category.procurement_controlled)

    def pending_approvals(self):
        return self.approvals.filter(status=Approval.Status.PENDING)

    @classmethod
    def start(cls, reservation, by, to_custodian, **details):
        """The requester turns a confirmed hold into a transfer (RQ-04 to RQ-05, RV-02 to RV-04)."""
        resource_request = reservation.request
        if by != resource_request.requester:
            raise BusinessRuleError(_("Only the requester can start this transfer."), reservation, "start transfer")
        if reservation.status != Reservation.Status.CONFIRMED:
            raise BusinessRuleError(_("The hold must be confirmed before a transfer starts."), reservation,
                                    "start transfer")
        if not to_custodian.has_role(Role.Code.ASSET_CUSTODIAN, resource_request.department):
            raise BusinessRuleError(_("The receiving custodian must be a custodian of your department."), reservation,
                                    "start transfer")
        if reservation.expires_at and reservation.expires_at < timezone.now():
            raise BusinessRuleError(_("This hold has expired (BR-12). Ask for a new hold."), reservation,
                                    "start transfer")
        if any(details.get(name) is not None and details[name] < 0
               for name in ("transfer_cost_aed", "distance_km", "van_trips")):
            raise BusinessRuleError(_("Costs, distances and van trips cannot be negative."), reservation,
                                    "start transfer")
        asset = Asset.objects.select_for_update().get(pk=reservation.listing.asset_id)
        transfer = cls.objects.create(
            asset=asset, request=resource_request, reservation=reservation, quantity=reservation.quantity,
            from_department=asset.owner_department, to_department=resource_request.department,
            to_custodian=to_custodian, created_by=by, **details,
        )
        asset.allocate(reservation.quantity)
        AuditLog.record(by, "transfer created", transfer, after="TR-01 Pending release approval")
        change_state(reservation, Reservation.Status.CONVERTED, by, "converted to transfer")
        change_state(resource_request, ResourceRequest.Status.IN_TRANSFER, by, "transfer created")
        Approval.open(Approval.Stage.TRANSFER_RELEASE, transfer, requested_by=by, department=transfer.from_department)
        return transfer

    def pending_stage(self, approval, action):
        """The approval being decided; Finance and Procurement may decide their stages in either order."""
        pending = self.pending_approvals()
        if approval is not None:
            pending = pending.filter(pk=approval.pk)
        approval = pending.first()
        if approval is None:
            raise BusinessRuleError(_("There is no approval task waiting on this transfer."), self, action)
        return approval

    def approve_stage(self, by, approval=None):
        """Approve a stage and move to the next one (release, receipt, then policy under BR-06)."""
        approval = self.pending_stage(approval, "approve transfer")
        approval.approve(by)
        if approval.stage == Approval.Stage.TRANSFER_RELEASE:
            change_state(self, self.Status.PENDING_RECEIPT, by, "release approved")
            Approval.open(Approval.Stage.TRANSFER_RECEIPT, self, requested_by=self.created_by,
                          department=self.to_department)
        elif approval.stage == Approval.Stage.TRANSFER_RECEIPT:
            if self.needs_finance() or self.needs_procurement():
                change_state(self, self.Status.PENDING_POLICY, by, "receipt approved")
                if self.needs_finance():
                    Approval.open(Approval.Stage.TRANSFER_FINANCE, self, requested_by=self.created_by)
                if self.needs_procurement():
                    Approval.open(Approval.Stage.TRANSFER_PROCUREMENT, self, requested_by=self.created_by)
            else:
                self.approver = by
                change_state(self, self.Status.APPROVED, by, "receipt approved", extra_fields=("approver",))
        elif not self.pending_approvals().exists():
            self.approver = by
            change_state(self, self.Status.APPROVED, by, "policy approved", extra_fields=("approver",))

    def reject_stage(self, by, reason, approval=None):
        approval = self.pending_stage(approval, "reject transfer")
        approval.reject(by, reason)
        change_state(self, self.Status.REJECTED, by, "rejected", reason)
        self._give_back(by, "transfer rejected")

    def cancel(self, by, reason):
        """Allowed only before handover; the held units return to the listing (FR-11.6)."""
        if not reason.strip():
            raise BusinessRuleError(_("Give a reason for cancelling (BR-20)."), self, "cancel transfer")
        if self.status not in (*self.WAITING, self.Status.APPROVED):
            raise BusinessRuleError(_("A transfer can only be cancelled before handover."), self, "cancel transfer")
        change_state(self, self.Status.CANCELLED, by, "cancelled", reason)
        self._give_back(by, "transfer cancelled")

    def _give_back(self, by, action):
        for approval in self.pending_approvals():
            approval.withdraw()
        asset = Asset.objects.select_for_update().get(pk=self.asset_id)
        asset.unallocate(self.quantity)
        self.reservation.listing.refresh_reserved_state(by)
        if self.request.status == ResourceRequest.Status.IN_TRANSFER:
            change_state(self.request, ResourceRequest.Status.OPEN, by, action)

    def check_custodian(self, by, department, action):
        if not by.has_role(Role.Code.ASSET_CUSTODIAN, department):
            raise BusinessRuleError(_("Only a custodian of %(department)s can do this.") % {"department": department},
                                    self, action)

    def hand_over(self, by, condition):
        """The releasing custodian records the handover (TR-04 to TR-05)."""
        self.check_custodian(by, self.from_department, "hand over")
        self.handed_over_at = timezone.now()
        self.handed_over_by = by
        self.handover_condition = condition
        change_state(self, self.Status.HANDED_OVER, by, "handed over",
                     extra_fields=("handed_over_at", "handed_over_by", "handover_condition"))
        if self.quantity == self.asset.quantity:
            change_state(self.asset, Asset.Status.IN_TRANSFER, by, "handed over")

    def confirm_receipt(self, by, received_quantity, received_condition):
        """The receiving custodian confirms; only now do owner, custody and location change (BR-13)."""
        self.check_custodian(by, self.to_department, "confirm receipt")
        if received_quantity != self.quantity or received_condition != self.handover_condition:
            raise BusinessRuleError(_("What arrived differs from the handover record. Record a discrepancy instead."),
                                    self, "confirm receipt")
        self._complete(by, received_quantity, received_condition, "receipt confirmed")

    def dispute(self, by, received_quantity, received_condition, note):
        self.check_custodian(by, self.to_department, "record discrepancy")
        if not note.strip():
            raise BusinessRuleError(_("Describe the difference (FR-11.5)."), self, "record discrepancy")
        if not 0 <= received_quantity <= self.quantity:
            raise BusinessRuleError(_("The received quantity must be between 0 and %(count)s.") % {"count": self.quantity},
                                    self, "record discrepancy")
        self.received_quantity = received_quantity
        self.received_condition = received_condition
        self.dispute_note = note
        change_state(self, self.Status.DISPUTED, by, "difference recorded", note,
                     extra_fields=("received_quantity", "received_condition", "dispute_note"))

    def resolve_dispute(self, by, accept, reason):
        """The receiving department representative accepts the delivery or returns it."""
        if not by.has_role(Role.Code.DEPARTMENT_REPRESENTATIVE, self.to_department):
            raise BusinessRuleError(_("Only the representative of %(department)s can resolve this.") % {
                "department": self.to_department}, self, "resolve dispute")
        if not reason.strip():
            raise BusinessRuleError(_("Give a reason for the resolution."), self, "resolve dispute")
        if accept:
            # A condition difference can be accepted; missing units cannot, so the delivery goes back instead.
            if self.received_quantity is not None and self.received_quantity != self.quantity:
                raise BusinessRuleError(_("Units are missing, so this delivery cannot be accepted. Return it instead."),
                                        self, "resolve dispute")
            self._complete(by, self.quantity, self.received_condition or self.handover_condition,
                           "resolved and received", reason)
        else:
            change_state(self, self.Status.CANCELLED, by, "returned", reason)
            asset = Asset.objects.select_for_update().get(pk=self.asset_id)
            if asset.status == Asset.Status.IN_TRANSFER:
                change_state(asset, asset.previous_status or Asset.Status.IN_STORAGE, by, "returned after dispute")
            asset.unallocate(self.quantity)
            self.reservation.listing.refresh_reserved_state(by)
            if self.request.status == ResourceRequest.Status.IN_TRANSFER:
                change_state(self.request, ResourceRequest.Status.OPEN, by, "transfer returned")

    def _complete(self, by, received_quantity, received_condition, action, reason=""):
        from sustainability.models import SustainabilityImpact

        self.received_at = timezone.now()
        self.received_by = by
        self.received_quantity = received_quantity
        self.received_condition = received_condition
        asset = Asset.objects.select_for_update().get(pk=self.asset_id)
        whole_record = self.quantity == asset.quantity
        if whole_record:
            # The whole record moves to the receiving department.
            asset.owner_department = self.to_department
            asset.custodian = self.to_custodian
            asset.campus, asset.building, asset.room = self.to_campus, self.to_building, self.to_room
            asset.condition = received_condition
            asset.allocated_qty = 0
            asset.available_qty = asset.quantity
            asset.save()
            if asset.status != Asset.Status.IN_SERVICE:
                change_state(asset, Asset.Status.IN_SERVICE, by, "received by new owner",
                             f"Now owned by {self.to_department}")
            else:  # already in service (for example after an earlier partial transfer)
                AuditLog.record(by, "received by new owner", asset, reason=f"Now owned by {self.to_department}")
            self.received_asset = asset
        else:
            # Only some units move: they become a new asset record of the receiving department.
            asset.allocated_qty -= self.quantity
            asset.quantity -= self.quantity
            asset.save(update_fields=["allocated_qty", "quantity"])
            # Keep the type: an IT record keeps "stores data" (data erasure, BR-09), furniture keeps its details.
            # Serial numbers stay with the units that did not move.
            model, extra = Asset, {}
            it, furniture = ITAsset.objects.filter(pk=asset.pk).first(), FurnitureAsset.objects.filter(pk=asset.pk).first()
            if it is not None:
                model, extra = ITAsset, {"stores_data": it.stores_data}
            elif furniture is not None:
                model, extra = FurnitureAsset, {"material": furniture.material, "dimensions": furniture.dimensions}
            new_asset = model.objects.create(**extra,
                name=asset.name, description=asset.description, category=asset.category, tags=asset.tags,
                condition=received_condition, status=Asset.Status.IN_SERVICE, quantity=self.quantity,
                available_qty=self.quantity, specifications=asset.specifications, campus=self.to_campus,
                building=self.to_building, room=self.to_room, value=asset.value, purchase_date=asset.purchase_date,
                planned_retirement_date=asset.planned_retirement_date, verified_on=timezone.now(), verified_by=by,
                owner_department=self.to_department, custodian=self.to_custodian, registered_by=asset.registered_by,
            )
            AuditLog.record(by, f"received from {asset.code} by {self.code}", new_asset, after="AS-02 In service")
            AuditLog.record(by, f"{self.quantity} unit(s) moved to {new_asset.code}", asset, reason=self.code)
            self.received_asset = asset = new_asset
        change_state(self, self.Status.COMPLETED, by, action, reason,
                     extra_fields=("received_at", "received_by", "received_quantity", "received_condition",
                                   "received_asset"))
        change_state(self.request, ResourceRequest.Status.FULFILLED, by, "receipt confirmed")
        listing = self.reservation.listing
        # Close only when every listed unit has really moved: other confirmed holds or running transfers
        # on the same listing keep it open (LS-06 means "all offered quantity has been transferred").
        still_running = listing.reservations.exclude(pk=self.reservation_id).filter(
            Q(status=Reservation.Status.CONFIRMED)
            | (Q(status=Reservation.Status.CONVERTED) & ~Q(transfer__status__in=Transfer.FINAL))).exists()
        if listing.status in (Listing.Status.PUBLISHED, Listing.Status.FULLY_RESERVED) and (
                whole_record or (listing.remaining_quantity() == 0 and not still_running)):
            change_state(listing, Listing.Status.CLOSED, by, "closed after transfer")
            for hold in listing.reservations.filter(status=Reservation.Status.REQUESTED):
                hold.cancel(by, "The listing closed after a transfer")
        SustainabilityImpact.record_transfer(self)


def expire_overdue():
    """BR-12 and FR-07: confirmed holds past their end, and open requests past their required-by date,
    expire. Run on the pages that show holds, and by the expire_overdue command."""
    for hold in Reservation.objects.filter(status=Reservation.Status.CONFIRMED, expires_at__lt=timezone.now()):
        with transaction.atomic():
            hold.expire()
    for resource_request in ResourceRequest.objects.filter(status=ResourceRequest.Status.OPEN,
                                                           required_by__lt=timezone.localdate()):
        with transaction.atomic():
            resource_request.expire()
