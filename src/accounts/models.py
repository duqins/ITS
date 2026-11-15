"""Department, User, Role and UserRole from the class diagram (design section 10)."""

from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied
from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=12, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def deactivate(self):
        # A department in use is never deleted, only deactivated (FR-03).
        self.is_active = False
        self.save(update_fields=["is_active"])


class Role(models.Model):
    """One of the nine user classes from SRS section 2.2."""

    class Code(models.TextChoices):
        DEPARTMENT_REPRESENTATIVE = "department_representative", "Department representative"
        ASSET_CUSTODIAN = "asset_custodian", "Asset custodian"
        REQUESTER = "requester", "Requester"
        BUSINESS_ADMINISTRATOR = "business_administrator", "Business administrator"
        PROCUREMENT_OFFICER = "procurement_officer", "Procurement officer"
        FINANCE_OFFICER = "finance_officer", "Finance officer"
        MAINTENANCE_STAFF = "maintenance_staff", "Maintenance staff"
        SUSTAINABILITY_OFFICER = "sustainability_officer", "Sustainability officer"
        SYSTEM_ADMINISTRATOR = "system_administrator", "System administrator"

    # What each role may do, from the access matrix in design section 6.
    # The server checks these actions on every request; hiding a button is not enough.
    ACTIONS = {
        Code.DEPARTMENT_REPRESENTATIVE: {
            "asset.view", "asset.register", "asset.confirm", "listing.prepare", "listing.publish",
            "listing.search", "request.approve", "match.view", "hold.confirm",
            "transfer.view", "transfer.approve_release", "transfer.approve_receipt",
            "history.view", "report.view", "dashboard.view", "ai.review_classification",
        },
        Code.ASSET_CUSTODIAN: {
            "asset.view", "asset.register", "asset.confirm", "listing.prepare", "listing.search",
            "match.view", "hold.confirm", "transfer.view", "transfer.handover", "transfer.receive",
            "history.view", "ai.review_classification",
        },
        Code.REQUESTER: {
            "listing.search", "request.submit", "match.choose", "hold.request",
            "transfer.start", "transfer.view",
        },
        Code.BUSINESS_ADMINISTRATOR: {
            "asset.view", "listing.search", "transfer.view", "history.view", "audit.view",
            "report.view", "dashboard.view", "report.review", "role.authorise",
        },
        Code.PROCUREMENT_OFFICER: {
            "asset.view", "listing.search", "transfer.view", "transfer.approve_procurement",
            "history.view", "report.view", "dashboard.view",
        },
        Code.FINANCE_OFFICER: {
            "asset.view", "listing.search", "transfer.view", "transfer.approve_finance",
            "history.view", "report.view", "dashboard.view", "report.review",
        },
        Code.MAINTENANCE_STAFF: {"asset.view", "listing.search", "history.view"},
        Code.SUSTAINABILITY_OFFICER: {
            "asset.view", "listing.search", "history.view", "report.view", "dashboard.view",
            "report.review",
        },
        Code.SYSTEM_ADMINISTRATOR: {"listing.search", "role.apply"},
    }

    code = models.CharField(max_length=40, choices=Code.choices, unique=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.get_code_display()

    @property
    def name(self):
        return self.get_code_display()

    def allows(self, action):
        return action in self.ACTIONS.get(self.code, set())


class User(AbstractUser):
    class AccountStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        BLOCKED = "blocked", "Blocked"

    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, null=True, blank=True, related_name="employees"
    )
    account_status = models.CharField(
        max_length=10, choices=AccountStatus.choices, default=AccountStatus.ACTIVE
    )
    failed_sign_ins = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def display_name(self):
        return str(self)

    def is_locked(self):
        return self.locked_until is not None and self.locked_until > timezone.now()

    def sign_in(self, password):
        """Check a password and apply the lockout rule: 5 failed sign-ins lock the account for 15 minutes."""
        rules = settings.DAWRA
        if self.account_status != self.AccountStatus.ACTIVE or self.is_locked():
            return False
        if self.check_password(password):
            self.failed_sign_ins = 0
            self.locked_until = None
            self.save(update_fields=["failed_sign_ins", "locked_until"])
            return True
        self.failed_sign_ins += 1
        if self.failed_sign_ins >= rules["MAX_FAILED_SIGN_INS"]:
            self.locked_until = timezone.now() + timedelta(minutes=rules["LOCKOUT_MINUTES"])
            self.failed_sign_ins = 0
        self.save(update_fields=["failed_sign_ins", "locked_until"])
        return False

    def active_user_roles(self):
        return self.user_roles.filter(status=UserRole.Status.ACTIVE).select_related("role", "department")

    def has_role(self, role_code, department=None):
        roles = self.active_user_roles().filter(role__code=role_code)
        if department is not None:
            roles = roles.filter(department=department)
        return roles.exists()

    def deactivate(self):
        self.account_status = self.AccountStatus.INACTIVE
        self.is_active = False
        self.save(update_fields=["account_status", "is_active"])


class UserRole(models.Model):
    """A role a user holds for one department (composition: User owns UserRole)."""

    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        AUTHORISED = "authorised", "Authorised"
        ACTIVE = "active", "Active"
        REMOVED = "removed", "Removed"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="assignments")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="user_roles")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.REQUESTED)
    authorised_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    applied_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "role", "department"], name="unique_role_per_department")
        ]
        ordering = ["role__code", "department__name"]

    def __str__(self):
        return f"{self.role} · {self.department}"

    def authorise(self, by):
        # Business administrator authorises; System administrator applies (FR-02, BR-01).
        if not by.has_role(Role.Code.BUSINESS_ADMINISTRATOR):
            raise PermissionDenied("Only a Business administrator can authorise a role.")
        self.status = self.Status.AUTHORISED
        self.authorised_by = by
        self.save(update_fields=["status", "authorised_by"])

    def apply(self, by):
        if not by.has_role(Role.Code.SYSTEM_ADMINISTRATOR):
            raise PermissionDenied("Only a System administrator can apply a role.")
        if self.status != self.Status.AUTHORISED:
            raise PermissionDenied("A role must be authorised before it is applied.")
        self.status = self.Status.ACTIVE
        self.applied_by = by
        self.save(update_fields=["status", "applied_by"])

    def remove(self):
        self.status = self.Status.REMOVED
        self.save(update_fields=["status"])

    def allows(self, action):
        return self.status == self.Status.ACTIVE and self.role.allows(action)
