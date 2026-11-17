"""C9 Basic report: requests and transfers with filters, totals and CSV export (FR-17)."""

import codecs
import csv
from collections import Counter
from datetime import date, datetime, time
from urllib.parse import urlencode

from django import forms
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy

from accounts.models import Department, Role
from accounts.permissions import role_required
from resource_requests.models import ResourceRequest
from transfers.models import Transfer


class ReportFilter(forms.Form):
    TYPES = [("requests", gettext_lazy("Requests")), ("transfers", gettext_lazy("Transfers"))]
    report = forms.ChoiceField(choices=TYPES, label=gettext_lazy("Report type"))
    date_from = forms.DateField(label=gettext_lazy("From"),
                                widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))
    date_to = forms.DateField(label=gettext_lazy("To"), widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))
    department = forms.ModelChoiceField(Department.objects.filter(is_active=True), required=False,
                                        label=gettext_lazy("Department"), empty_label=gettext_lazy("All departments"))

    def clean(self):
        data = super().clean()
        if data.get("date_from") and data.get("date_to") and data["date_from"] > data["date_to"]:
            raise forms.ValidationError(_("Choose a start date on or before the end date, then apply again."))
        return data


def safe_cell(value):
    """Stop spreadsheet programs from running text that starts like a formula."""
    text = "" if value is None else str(value)
    return "'" + text if text[:1] in ("=", "+", "-", "@") else text


def zone_range(data):
    zone = timezone.get_current_timezone()
    return datetime.combine(data["date_from"], time.min, zone), datetime.combine(data["date_to"], time.max, zone)


def request_rows(start, end, department):
    rows = ResourceRequest.objects.filter(created_at__range=(start, end)).exclude(status=ResourceRequest.Status.DRAFT)
    if department:
        rows = rows.filter(department=department)
    header = [_("Request"), _("Purpose"), _("Requester"), _("Department"), _("Category"), _("Quantity"),
              _("Required by"), _("Status"), _("Submitted")]
    data = [[r.code, r.purpose, str(r.requester), str(r.department), str(r.category), r.quantity, r.required_by,
             r.get_status_display(), timezone.localtime(r.submitted_at).date() if r.submitted_at else ""]
            for r in rows.select_related("requester", "department", "category")]
    return header, data, Counter(r.get_status_display() for r in rows)


def transfer_rows(start, end, department):
    rows = Transfer.objects.filter(created_at__range=(start, end))
    if department:
        rows = rows.filter(Q(from_department=department) | Q(to_department=department))
    header = [_("Transfer"), _("Asset"), _("Quantity"), _("From"), _("To"), _("Status"), _("Final approver"),
              _("Handed over"), _("Received")]
    # Dates stay dates: the page shows them like every other date and the CSV writes them as YYYY-MM-DD.
    fmt = lambda d: timezone.localtime(d).date() if d else ""  # noqa: E731
    data = [[t.code, f"{t.asset.code} {t.asset.name}", t.quantity, str(t.from_department), str(t.to_department),
             t.get_status_display(), str(t.approver or ""), fmt(t.handed_over_at), fmt(t.received_at)]
            for t in rows.select_related("asset", "from_department", "to_department", "approver")]
    return header, data, Counter(t.get_status_display() for t in rows)


@role_required("report.view")
def index(request):
    today = timezone.localdate()
    # Start from the default filters and lay the chosen ones on top, so "?format=csv" alone still works.
    params = {"report": "requests", "date_from": date(today.year, 1, 1).isoformat(), "date_to": today.isoformat(),
              **{key: value for key, value in request.GET.items() if key != "format"}}
    form = ReportFilter(params)
    role = request.active_role
    own_only = role.role.code == Role.Code.DEPARTMENT_REPRESENTATIVE
    if own_only:  # representatives report on their own department only
        form.fields["department"].queryset = Department.objects.filter(pk=role.department_id)
        form.fields["department"].empty_label = None
    context = {"form": form, "header": [], "rows": [], "totals": {}, "query": urlencode(params)}
    if form.is_valid():
        data = form.cleaned_data
        department = role.department if own_only else data["department"]
        start, end = zone_range(data)
        builder = request_rows if data["report"] == "requests" else transfer_rows
        header, rows, totals = builder(start, end, department)
        if request.GET.get("format") == "csv":
            return csv_response(data, department, header, rows, totals)
        context.update(header=header, rows=rows, totals=dict(totals), title=dict(ReportFilter.TYPES)[data["report"]])
    return render(request, "reports/index.html", context)


def csv_response(data, department, header, rows, totals):
    """The export contains the filters, the records and the totals (SI-04)."""
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response.write(codecs.BOM_UTF8)  # lets Excel read Arabic text as UTF-8
    response["Content-Disposition"] = f'attachment; filename="dawra-{data["report"]}-{data["date_from"]}-{data["date_to"]}.csv"'
    writer = csv.writer(response)
    writer.writerow([_("Report"), str(dict(ReportFilter.TYPES)[data["report"]])])
    writer.writerow([_("Period"), data["date_from"], data["date_to"]])
    writer.writerow([_("Department"), department or _("All departments")])
    writer.writerow([_("Data"), _("Synthetic demo data")])
    writer.writerow([])
    writer.writerow(header)
    writer.writerows([[safe_cell(cell) for cell in row] for row in rows])
    writer.writerow([])
    writer.writerow([_("Total records"), len(rows)])
    for status, count in sorted(totals.items()):
        writer.writerow([status, count])
    return response
