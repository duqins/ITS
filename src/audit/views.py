"""C6 States and history: who did what, and when."""

import csv
from datetime import datetime, time

from django import forms
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from accounts.models import Role
from accounts.permissions import role_required
from assets.models import Asset

from .models import AuditLog


def safe_cell(value):
    """Stop spreadsheet programs from running text that starts like a formula."""
    text = str(value)
    return "'" + text if text[:1] in ("=", "+", "-", "@") else text


def asset_records(asset):
    """Every record whose history belongs to this asset: listings, holds, transfers, approvals, AI suggestions."""
    from transfers.models import Approval, Reservation, Transfer

    listing_ids = list(asset.listings.values_list("pk", flat=True))
    transfer_ids = list(Transfer.objects.filter(Q(asset=asset) | Q(received_asset=asset)).values_list("pk", flat=True))
    return {
        "asset": [asset.pk],
        "listing": listing_ids,
        "reservation": list(Reservation.objects.filter(listing__in=listing_ids).values_list("pk", flat=True)),
        "transfer": transfer_ids,
        "approval": list(Approval.objects.filter(Q(listing__in=listing_ids) | Q(transfer__in=transfer_ids))
                         .values_list("pk", flat=True)),
        "aisuggestion": list(asset.ai_suggestions.values_list("pk", flat=True)),
    }


@role_required("history.view")
def asset_history(request, pk):
    asset = get_object_or_404(Asset.objects.select_related("owner_department"), pk=pk)
    role = request.active_role
    if role.role.code in (Role.Code.ASSET_CUSTODIAN, Role.Code.DEPARTMENT_REPRESENTATIVE) \
            and role.department_id != asset.owner_department_id:
        raise PermissionDenied("Custodians and representatives see the history of their own department's assets.")
    query = Q()
    for record_type, ids in asset_records(asset).items():
        if ids:
            query |= Q(record_type=record_type, record_id__in=ids)
    entries = AuditLog.objects.filter(query).select_related("user").order_by("created_at", "id")
    return render(request, "audit/asset_history.html", {"asset": asset, "entries": entries})


class AuditFilter(forms.Form):
    user = forms.CharField(required=False, label="User name contains")
    record_type = forms.ChoiceField(required=False, label="Record type")
    action = forms.CharField(required=False, label="Action contains")
    date_from = forms.DateField(required=False, label="From", widget=forms.DateInput(attrs={"type": "date"}))
    date_to = forms.DateField(required=False, label="To", widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        types = AuditLog.objects.order_by().values_list("record_type", flat=True).distinct()
        self.fields["record_type"].choices = [("", "Any record")] + [(t, t) for t in sorted(set(types))]

    def clean(self):
        data = super().clean()
        if data.get("date_from") and data.get("date_to") and data["date_from"] > data["date_to"]:
            raise forms.ValidationError("Choose a start date on or before the end date.")
        return data

    def apply(self, entries):
        data = self.cleaned_data
        if data["user"]:
            entries = entries.filter(Q(user__username__icontains=data["user"]) | Q(user__first_name__icontains=data["user"])
                                     | Q(user__last_name__icontains=data["user"]))
        if data["record_type"]:
            entries = entries.filter(record_type=data["record_type"])
        if data["action"]:
            entries = entries.filter(action__icontains=data["action"])
        zone = timezone.get_current_timezone()
        if data["date_from"]:
            entries = entries.filter(created_at__gte=datetime.combine(data["date_from"], time.min, zone))
        if data["date_to"]:
            entries = entries.filter(created_at__lte=datetime.combine(data["date_to"], time.max, zone))
        return entries


@role_required("audit.view")
def audit_search(request):
    """Search the audit log; CSV export leaves the entries unchanged (FR-18.3)."""
    form = AuditFilter(request.GET or None)
    entries = AuditLog.objects.select_related("user")
    if form.is_valid():
        entries = form.apply(entries)
    if request.GET.get("format") == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="dawra-audit-log.csv"'
        writer = csv.writer(response)
        writer.writerow(["time", "user", "role", "action", "record type", "record id", "before", "after", "reason"])
        for e in entries:
            writer.writerow([safe_cell(v) for v in (
                timezone.localtime(e.created_at).strftime("%Y-%m-%d %H:%M"), e.user or "system", e.role, e.action,
                e.record_type, e.record_id, e.before_value, e.after_value, e.reason)])
        return response
    return render(request, "audit/audit_search.html", {"form": form, "entries": entries[:200],
                                                       "total": entries.count(), "query": request.GET.urlencode()})
