"""C4 Request and track."""

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.http import require_POST

from accounts.models import Role
from accounts.permissions import role_required
from audit.models import AuditLog
from core.actions import perform

from .forms import RequestForm
from .models import ResourceRequest

# Stages shown above a request, and which statuses belong to each.
JOURNEY = [
    (gettext_lazy("Draft"), ("RQ-01",)),
    (gettext_lazy("Department review"), ("RQ-02",)),
    (gettext_lazy("Find a match"), ("RQ-03",)),
    (gettext_lazy("Hold"), ("RQ-04",)),
    (gettext_lazy("Transfer"), ("RQ-05",)),
    (gettext_lazy("Fulfilled"), ("RQ-06",)),
]


def visible_requests(request):
    role = request.active_role
    if role.role.code == Role.Code.DEPARTMENT_REPRESENTATIVE:
        # A representative sees the submitted requests of their department.
        return ResourceRequest.objects.filter(department=role.department).exclude(status=ResourceRequest.Status.DRAFT)
    return ResourceRequest.objects.filter(requester=request.user)


def get_visible_request(request, pk):
    obj = get_object_or_404(ResourceRequest.objects.select_related("category", "requester", "department"), pk=pk)
    role = request.active_role
    if obj.requester_id == request.user.pk:
        return obj
    if role.role.code == Role.Code.DEPARTMENT_REPRESENTATIVE and role.department_id == obj.department_id:
        return obj
    raise PermissionDenied(_("You can only open your own requests or your department's requests."))


@role_required("request.submit", "request.approve")
def request_list(request):
    requests = visible_requests(request).select_related("category", "requester")
    status = request.GET.get("status", "")
    if status in ResourceRequest.Status.values:
        requests = requests.filter(status=status)
    return render(request, "resource_requests/request_list.html", {
        "requests": requests, "statuses": ResourceRequest.Status.choices, "status": status,
        "can_create": request.active_role.allows("request.submit"),
    })


@role_required("request.submit")
def request_create(request):
    initial = {"purpose": request.GET.get("purpose", "")}
    if request.GET.get("category", "").isdigit():
        initial["category"] = int(request.GET["category"])
    form = RequestForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.requester = request.user
        obj.department = request.active_role.department

        def create():
            obj.save()
            AuditLog.record(request.user, "created", obj, after="RQ-01 Draft")
            if request.POST.get("submit_for") == "approval":
                obj.submit(request.user)

        if perform(request, create, _("Request saved.")):
            return redirect("resource_requests:detail", pk=obj.pk)
    return render(request, "resource_requests/request_form.html", {"form": form,
                                                                   "title": _("Submit a resource request")})


@role_required("request.submit")
def request_edit(request, pk):
    obj = get_visible_request(request, pk)
    if obj.requester_id != request.user.pk or obj.status != ResourceRequest.Status.DRAFT:
        messages.error(request, _("Only your own draft can be edited."))
        return redirect("resource_requests:detail", pk=obj.pk)
    form = RequestForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        AuditLog.record(request.user, "draft edited", obj, reason=", ".join(form.changed_data))
        if request.POST.get("submit_for") == "approval":
            perform(request, lambda: obj.submit(request.user), _("Sent to your department representative."))
        else:
            messages.success(request, _("Draft saved."))
        return redirect("resource_requests:detail", pk=obj.pk)
    return render(request, "resource_requests/request_form.html", {"form": form, "title": _("Edit %(code)s") % {
        "code": obj.code}, "obj": obj})


@role_required("request.submit", "request.approve")
def request_detail(request, pk):
    obj = get_visible_request(request, pk)
    mine = obj.requester_id == request.user.pk
    current = next((i for i, (_, codes) in enumerate(JOURNEY) if obj.status in codes), None)
    last_decision = obj.approvals.exclude(status="AT-01").order_by("-decided_at").first()
    return render(request, "resource_requests/request_detail.html", {
        "obj": obj,
        "journey": [(label, current is not None and i < current, i == current) for i, (label, _) in enumerate(JOURNEY)],
        "pending": obj.pending_approval(),
        "last_decision": last_decision,
        "updates": AuditLog.for_record(obj)[:20],
        "mine": mine,
        "can_edit": mine and obj.status == ResourceRequest.Status.DRAFT,
        "can_cancel": mine and obj.status in ResourceRequest.ACTIVE,
        "can_close": mine and obj.status == ResourceRequest.Status.OPEN,
    })


@require_POST
@role_required("request.submit")
def request_submit(request, pk):
    obj = get_visible_request(request, pk)
    if obj.requester_id != request.user.pk:
        raise PermissionDenied(_("Only the requester can submit this request."))
    perform(request, lambda: obj.submit(request.user), _("Sent to your department representative for approval."))
    return redirect("resource_requests:detail", pk=obj.pk)


@require_POST
@role_required("request.submit")
def request_cancel(request, pk):
    obj = get_visible_request(request, pk)
    if obj.requester_id != request.user.pk:
        raise PermissionDenied(_("Only the requester can cancel this request."))
    perform(request, lambda: obj.cancel(request.user, request.POST.get("reason", "").strip()), _("Request cancelled."))
    return redirect("resource_requests:detail", pk=obj.pk)


@require_POST
@role_required("request.submit")
def request_close(request, pk):
    obj = get_visible_request(request, pk)
    if obj.requester_id != request.user.pk:
        raise PermissionDenied(_("Only the requester can close this request."))
    reason = request.POST.get("reason", "").strip() or "No suitable item found"
    perform(request, lambda: obj.close_no_suitable_item(request.user, reason),
            _("Closed as no suitable item. It does not count as an avoided purchase."))
    return redirect("resource_requests:detail", pk=obj.pk)
