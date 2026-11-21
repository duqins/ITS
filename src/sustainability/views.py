"""C7 Sustainability dashboard."""

from datetime import date

from django import forms
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy

from accounts.models import Department, Role
from accounts.permissions import role_required
from core.actions import perform

from .charts import savings_chart
from .indicators import SustainabilityIndicators
from .models import SustainabilityImpact


class DashboardFilter(forms.Form):
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


def dashboard_scope(request):
    """Returns (filter form, indicators); a representative only sees their own department."""
    today = timezone.localdate()
    defaults = {"date_from": date(today.year, 1, 1).isoformat(), "date_to": today.isoformat()}
    form = DashboardFilter(request.GET or defaults)
    role = request.active_role
    own_only = role.role.code == Role.Code.DEPARTMENT_REPRESENTATIVE
    if own_only:
        form.fields["department"].queryset = Department.objects.filter(pk=role.department_id)
        form.fields["department"].empty_label = None
    if form.is_valid():
        data = form.cleaned_data
        department = role.department if own_only else data["department"]
        return form, SustainabilityIndicators(data["date_from"], data["date_to"], department)
    return form, None


@role_required("dashboard.view")
def dashboard(request):
    form, scope = dashboard_scope(request)
    role = request.active_role
    pending = SustainabilityImpact.objects.none()
    if role.role.code == Role.Code.DEPARTMENT_REPRESENTATIVE:
        pending = SustainabilityImpact.objects.filter(department=role.department, purchase_avoided_confirmed=False)
    return render(request, "sustainability/dashboard.html", {
        "form": form,
        "indicators": scope.indicators() if scope else [],
        "chart": savings_chart(scope.savings_by_month()) if scope else None,
        "scope": scope,
        "pending": pending.select_related("transfer__asset"),
    })


@require_POST
@role_required("dashboard.view")
def confirm_avoided_purchase(request, pk):
    impact = get_object_or_404(SustainabilityImpact.objects.select_related("transfer"), pk=pk)
    if request.active_role.department_id != impact.department_id:
        raise PermissionDenied(_("Only the receiving department representative can confirm this."))
    perform(request, lambda: impact.confirm_avoided_purchase(request.user),
            _("Avoided purchase confirmed. It now counts on the dashboard."))
    target = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}):
        return redirect(target)
    return redirect("sustainability:dashboard")
