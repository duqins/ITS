"""Category, Asset (with ITAsset and FurnitureAsset) and Listing from the class diagram."""

from datetime import date

from django.conf import settings
from django.db import models
from django.db.models import F, Q, Sum
from django.utils import timezone

from accounts.models import Department, Role
from audit.lifecycle import BusinessRuleError, change_state
from audit.models import AuditLog


class Condition(models.TextChoices):
    NEW = "new", "New"
    GOOD = "good", "Good"
    FAIR = "fair", "Fair"
    POOR = "poor", "Poor"
    NOT_WORKING = "not_working", "Not working"

    @classmethod
    def rank(cls, value):
        """New = 4 down to Not working = 0, so conditions can be compared."""
        order = [cls.NOT_WORKING, cls.POOR, cls.FAIR, cls.GOOD, cls.NEW]
        return order.index(value) if value in order else -1


class Category(models.Model):
    class Unit(models.TextChoices):
        ITEM = "item", "Item"
        SET = "set", "Set"
        KILOGRAM = "kilogram", "Kilogram"

    name = models.CharField(max_length=80)
    subcategory = models.CharField(max_length=80, blank=True)
    unit = models.CharField(max_length=10, choices=Unit.choices, default=Unit.ITEM)
    procurement_controlled = models.BooleanField(default=False)
    special_handling = models.BooleanField(default=False)
    # Carbon factors per unit (design section 12, Table 12.3). Empty means N/A.
    emission_factor_low = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    emission_factor_high = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    factor_source = models.CharField(max_length=255, blank=True)
    factor_version = models.CharField(max_length=40, blank=True)
    # Added in Phase 6 so waste diverted (kg) and avoided purchases (AED) can be calculated (F3, F7).
    unit_mass_kg = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    replacement_cost_aed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    replacement_cost_source = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name", "subcategory"]
        verbose_name_plural = "categories"
        constraints = [models.UniqueConstraint(fields=["name", "subcategory"], name="unique_category")]

    def __str__(self):
        return f"{self.name} / {self.subcategory}" if self.subcategory else self.name

    def is_special_handling(self):
        return self.special_handling


class Asset(models.Model):
    class Status(models.TextChoices):
        DRAFT = "AS-01", "Draft"
        IN_SERVICE = "AS-02", "In service"
        IN_STORAGE = "AS-03", "In storage"
        UNDER_MAINTENANCE = "AS-04", "Under maintenance"
        IN_TRANSFER = "AS-05", "In transfer"
        RETIRED = "AS-06", "Retired"
        DONATED = "AS-07", "Donated"
        RECYCLED = "AS-08", "Recycled"
        DISASSEMBLED = "AS-09", "Disassembled"
        DISPOSED = "AS-10", "Disposed"

    ACTIVE = (Status.IN_SERVICE, Status.IN_STORAGE)
    # Allowed moves from the asset state diagram (Figure 10.2, SRS Table 4.3).
    TRANSITIONS = {
        Status.DRAFT: {Status.IN_SERVICE, Status.IN_STORAGE},
        Status.IN_SERVICE: {Status.IN_STORAGE, Status.UNDER_MAINTENANCE, Status.IN_TRANSFER, Status.RETIRED},
        Status.IN_STORAGE: {Status.IN_SERVICE, Status.UNDER_MAINTENANCE, Status.IN_TRANSFER, Status.RETIRED},
        Status.UNDER_MAINTENANCE: {Status.IN_SERVICE, Status.IN_STORAGE, Status.RETIRED},
        Status.IN_TRANSFER: {Status.IN_SERVICE, Status.IN_STORAGE},
        Status.RETIRED: {Status.IN_SERVICE, Status.IN_STORAGE, Status.DONATED, Status.RECYCLED,
                         Status.DISASSEMBLED, Status.DISPOSED},
    }

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    # A draft may be saved before the category is known; confirmation needs it.
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name="assets")
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated search tags")
    condition = models.CharField(max_length=12, choices=Condition.choices, default=Condition.GOOD)
    status = models.CharField(max_length=5, choices=Status.choices, default=Status.DRAFT)
    previous_status = models.CharField(max_length=5, choices=Status.choices, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    available_qty = models.PositiveIntegerField(default=1)
    reserved_qty = models.PositiveIntegerField(default=0)
    allocated_qty = models.PositiveIntegerField(default=0)
    specifications = models.TextField(blank=True)
    # Location is a composite of campus, building and room (section 8).
    campus = models.CharField(max_length=60, default="Main campus")
    building = models.CharField(max_length=60, blank=True)
    room = models.CharField(max_length=30, blank=True)
    value = models.DecimalField("estimated value (AED)", max_digits=10, decimal_places=2, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    planned_retirement_date = models.DateField(null=True, blank=True)
    revised_retirement_date = models.DateField(null=True, blank=True)
    verified_on = models.DateTimeField(null=True, blank=True)
    owner_department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="assets")
    custodian = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="custody_assets")
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            # BR-11: available + reserved + allocated never exceeds the quantity, so a unit
            # can never be reserved twice ("the last item cannot go to two people").
            models.CheckConstraint(
                condition=Q(quantity__gte=F("available_qty") + F("reserved_qty") + F("allocated_qty")),
                name="asset_quantities_within_total",
            ),
        ]

    def __str__(self):
        return f"AST-{self.pk:04d} {self.name}" if self.pk else self.name

    @property
    def code(self):
        return f"AST-{self.pk:04d}"

    @property
    def location(self):
        return ", ".join(p for p in (self.room, self.building, self.campus) if p)

    @property
    def asset_age(self):
        """Derived attribute /assetAge in whole years; not stored (section 8)."""
        if not self.purchase_date:
            return None
        today = date.today()
        return today.year - self.purchase_date.year - (
            (today.month, today.day) < (self.purchase_date.month, self.purchase_date.day)
        )

    @property
    def is_active(self):
        return self.status in self.ACTIVE

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    def register(self, by, department):
        """Save a new asset as Draft (AS-01) with the registering user as custodian."""
        self.owner_department = department
        self.custodian = by
        self.registered_by = by
        self.status = self.Status.DRAFT
        self.available_qty = self.quantity
        self.save()
        AuditLog.record(by, "registered", self, after="AS-01 Draft")

    def confirm(self, by, in_use=True):
        """A second user confirms the record; the asset becomes Active (AS-02 or AS-03)."""
        if by == self.registered_by:
            raise BusinessRuleError("A different user must confirm this asset record (BR-02).", self, "confirm asset")
        if self.category_id is None:
            raise BusinessRuleError("Choose a category before the asset is confirmed.", self, "confirm asset")
        self.verified_on = timezone.now()
        self.verified_by = by
        change_state(self, self.Status.IN_SERVICE if in_use else self.Status.IN_STORAGE, by,
                     "confirmed", extra_fields=("verified_on", "verified_by"))

    def change_status(self, to, by, reason=""):
        change_state(self, to, by, "status changed", reason)

    def reserve(self, qty):
        if qty > self.available_qty:
            raise BusinessRuleError(
                f"Only {self.available_qty} of {self.code} are still available.", self, "reserve"
            )
        self.available_qty -= qty
        self.reserved_qty += qty
        self.save(update_fields=["available_qty", "reserved_qty"])

    def release(self, qty):
        """Give reserved units back (hold declined, cancelled or expired)."""
        self.reserved_qty -= qty
        self.available_qty += qty
        self.save(update_fields=["available_qty", "reserved_qty"])

    def allocate(self, qty):
        """A transfer was created for reserved units."""
        self.reserved_qty -= qty
        self.allocated_qty += qty
        self.save(update_fields=["reserved_qty", "allocated_qty"])

    def unallocate(self, qty):
        """A transfer was rejected or cancelled before handover."""
        self.allocated_qty -= qty
        self.available_qty += qty
        self.save(update_fields=["allocated_qty", "available_qty"])

    def verification_is_recent(self):
        limit = settings.DAWRA["VERIFICATION_MAX_AGE_DAYS"]
        return self.verified_on is not None and (timezone.now() - self.verified_on).days <= limit

    def can_be_managed_by(self, user_role):
        """Custodians and representatives act on their own department's assets only."""
        return (
            user_role is not None
            and user_role.department_id == self.owner_department_id
            and user_role.role.code in (Role.Code.ASSET_CUSTODIAN, Role.Code.DEPARTMENT_REPRESENTATIVE)
        )


class ITAsset(Asset):
    serial_number = models.CharField(max_length=60, blank=True)
    stores_data = models.BooleanField(default=False)

    class Meta:
        verbose_name = "IT asset"

    def needs_data_erasure(self):
        return self.stores_data


class FurnitureAsset(Asset):
    material = models.CharField(max_length=60, blank=True)
    dimensions = models.CharField(max_length=60, blank=True)

    class Meta:
        verbose_name = "furniture asset"


class Listing(models.Model):
    class Status(models.TextChoices):
        DRAFT = "LS-01", "Draft"
        PENDING_RELEASE = "LS-02", "Pending release approval"
        PUBLISHED = "LS-03", "Published"
        FULLY_RESERVED = "LS-04", "Fully reserved"
        WITHDRAWN = "LS-05", "Withdrawn"
        CLOSED = "LS-06", "Closed"

    class ReleaseReason(models.TextChoices):
        SURPLUS = "surplus", "Surplus"
        UNDERUTILISED = "underutilised", "Underutilised"
        UNWANTED = "unwanted", "Unwanted"

    TRANSITIONS = {
        Status.DRAFT: {Status.PENDING_RELEASE, Status.WITHDRAWN},
        Status.PENDING_RELEASE: {Status.PUBLISHED, Status.DRAFT, Status.WITHDRAWN},
        Status.PUBLISHED: {Status.FULLY_RESERVED, Status.WITHDRAWN, Status.CLOSED},
        Status.FULLY_RESERVED: {Status.PUBLISHED, Status.WITHDRAWN, Status.CLOSED},
    }

    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name="listings")
    quantity = models.PositiveIntegerField()
    available_from = models.DateField(default=date.today)
    restrictions = models.TextField(blank=True)
    release_reason = models.CharField(max_length=15, choices=ReleaseReason.choices, default=ReleaseReason.SURPLUS)
    status = models.CharField(max_length=5, choices=Status.choices, default=Status.DRAFT)
    version = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return f"LST-{self.pk:04d} {self.asset.name}" if self.pk else f"Listing of {self.asset.name}"

    @property
    def code(self):
        return f"LST-{self.pk:04d}"

    def held_quantity(self):
        from transfers.models import Reservation

        held = self.reservations.filter(status__in=Reservation.HOLDING).aggregate(total=Sum("quantity"))["total"]
        return held or 0

    def remaining_quantity(self):
        return max(0, min(self.quantity - self.held_quantity(), self.asset.available_qty))

    def submit_for_release(self, by):
        """Ask the owning department representative to release the listing (BR-04)."""
        from transfers.models import Approval

        if self.asset.status not in Asset.ACTIVE:
            raise BusinessRuleError("Only an asset that is in service or in storage can be listed.", self, "submit listing")
        if self.quantity > self.asset.available_qty:
            raise BusinessRuleError("The listing offers more units than are available.", self, "submit listing")
        change_state(self, self.Status.PENDING_RELEASE, by, "submitted for release")
        Approval.open(Approval.Stage.LISTING_RELEASE, self, requested_by=self.created_by,
                      department=self.asset.owner_department)

    def pending_approval(self):
        from transfers.models import Approval

        return self.approvals.filter(status=Approval.Status.PENDING).first()

    def publish(self, by):
        """The owning department representative approves the release; the listing is published."""
        approval = self.pending_approval()
        if approval is None:
            raise BusinessRuleError("This listing has no release request to approve.", self, "publish listing")
        approval.approve(by)
        self.published_at = timezone.now()
        change_state(self, self.Status.PUBLISHED, by, "published", extra_fields=("published_at",))

    def reject_release(self, by, reason):
        approval = self.pending_approval()
        if approval is None:
            raise BusinessRuleError("This listing has no release request to reject.", self, "reject listing")
        approval.reject(by, reason)
        change_state(self, self.Status.DRAFT, by, "release rejected", reason)

    def withdraw(self, by, reason):
        from transfers.models import Reservation, Transfer

        if not reason:
            raise BusinessRuleError("Give a reason for withdrawing the listing (BR-20).", self, "withdraw listing")
        active = Transfer.objects.filter(reservation__listing=self).exclude(status__in=Transfer.FINAL)
        if active.exists():
            raise BusinessRuleError("A listing cannot be withdrawn during a transfer (BR-19).", self, "withdraw listing")
        change_state(self, self.Status.WITHDRAWN, by, "withdrawn", reason)
        for reservation in self.reservations.filter(status__in=Reservation.OPEN):
            reservation.cancel(by, "Listing withdrawn")

    def refresh_reserved_state(self, by):
        """Fully reserved when nothing is left to hold; published again when units come back."""
        remaining = self.remaining_quantity()
        if self.status == self.Status.PUBLISHED and remaining == 0:
            change_state(self, self.Status.FULLY_RESERVED, by, "fully reserved")
        elif self.status == self.Status.FULLY_RESERVED and remaining > 0:
            change_state(self, self.Status.PUBLISHED, by, "units available again")
