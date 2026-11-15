"""SustainabilityImpact from the class diagram, with the formulas of design section 12 (C7)."""

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from accounts.models import Department

# F6: diesel van, average up to 3.5 t, UK DESNZ 2025 conversion factors.
VAN_KG_CO2E_PER_KM = Decimal("0.25561")
VAN_FACTOR_SOURCE = "UK DESNZ 2025, Diesel van, average (up to 3.5 t)"


class SustainabilityImpact(models.Model):
    class DataStatus(models.TextChoices):
        MEASURED = "measured", "Measured"
        ESTIMATED = "estimated", "Estimated"
        SYNTHETIC = "synthetic", "Synthetic"

    # In Phase 6 only completed transfers create impacts; repair and end-of-life come later.
    transfer = models.OneToOneField("transfers.Transfer", on_delete=models.PROTECT, related_name="impact")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="impacts")
    occurred_on = models.DateField(default=timezone.localdate)
    items_diverted = models.PositiveIntegerField()
    waste_diverted_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    replacement_cost_aed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    replacement_cost_source = models.CharField(max_length=255, blank=True)
    avoided_purchase_aed = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    transfer_cost_aed = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    transport_co2e_kg = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    co2e_low_kg = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    co2e_high_kg = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    factor_version = models.CharField(max_length=40, blank=True)
    data_status = models.CharField(max_length=10, choices=DataStatus.choices, default=DataStatus.SYNTHETIC)
    # BR-18: an avoided purchase counts only after the receiving representative confirms it.
    purchase_avoided_confirmed = models.BooleanField(default=False)
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="+"
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_on", "-id"]

    def __str__(self):
        return f"Impact of {self.transfer}"

    @classmethod
    def record_transfer(cls, transfer):
        impact = cls(transfer=transfer, department=transfer.to_department)
        impact.calculate()
        impact.save()
        return impact

    def calculate(self):
        """Fill the figures from the transfer and its category factors (Table 12.1)."""
        transfer = self.transfer
        category = transfer.asset.category
        items = transfer.received_quantity or transfer.quantity
        self.items_diverted = items
        self.transfer_cost_aed = transfer.transfer_cost_aed
        # Transport = van trips x km x 0.25561 (F6).
        self.transport_co2e_kg = Decimal(transfer.van_trips) * transfer.distance_km * VAN_KG_CO2E_PER_KM
        self.waste_diverted_kg = None
        self.avoided_purchase_aed = None
        self.co2e_low_kg = self.co2e_high_kg = None
        if category is None:
            return
        if category.unit_mass_kg is not None:
            self.waste_diverted_kg = items * category.unit_mass_kg
        if category.replacement_cost_aed is not None:
            self.replacement_cost_aed = category.replacement_cost_aed
            self.replacement_cost_source = category.replacement_cost_source
            self.avoided_purchase_aed = items * category.replacement_cost_aed
        # Carbon saved = quantity x category factor - transport, as a low-to-high range (N/A without a factor).
        if category.emission_factor_low is not None:
            self.co2e_low_kg = items * category.emission_factor_low - self.transport_co2e_kg
        if category.emission_factor_high is not None:
            self.co2e_high_kg = items * category.emission_factor_high - self.transport_co2e_kg
        self.factor_version = category.factor_version

    def confirm_avoided_purchase(self, by):
        from accounts.models import Role
        from audit.lifecycle import BusinessRuleError
        from audit.models import AuditLog

        if not by.has_role(Role.Code.DEPARTMENT_REPRESENTATIVE, self.department):
            raise BusinessRuleError(f"Only the representative of {self.department} can confirm this.", self.transfer,
                                    "confirm avoided purchase")
        self.purchase_avoided_confirmed = True
        self.confirmed_by = by
        self.confirmed_at = timezone.now()
        self.save(update_fields=["purchase_avoided_confirmed", "confirmed_by", "confirmed_at"])
        AuditLog.record(by, "avoided purchase confirmed", self.transfer, reason="BR-18")
