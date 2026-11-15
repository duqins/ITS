from django.contrib import admin

from .models import Approval, Reservation, Transfer


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ("__str__", "status", "department", "approver", "decided_at")
    list_filter = ("stage", "status")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "request", "listing", "quantity", "status", "expires_at")


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("__str__", "asset", "from_department", "to_department", "quantity", "status")
    list_filter = ("status",)
