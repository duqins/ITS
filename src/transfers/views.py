"""C5 Approve and transfer: approval tasks, holds and transfers."""

from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import Role
from accounts.permissions import check_action, role_required
from assets.models import Listing
from audit.models import AuditLog
from core.actions import perform
from resource_requests.models import ResourceRequest

from .forms import HandoverForm, ReceiptForm, TransferForm
from .models import Approval, Reservation, Transfer, expire_overdue

DECIDER_ACTIONS = ("request.approve", "listing.publish", "transfer.approve_release", "transfer.approve_receipt",
                   "transfer.approve_finance", "transfer.approve_procurement")
STAGE_ACTION = {
    Approval.Stage.REQUEST_DEPARTMENT: "request.approve",
    Approval.Stage.LISTING_RELEASE: "listing.publish",
    Approval.Stage.TRANSFER_RELEASE: "transfer.approve_release",
    Approval.Stage.TRANSFER_RECEIPT: "transfer.approve_receipt",
    Approval.Stage.TRANSFER_FINANCE: "transfer.approve_finance",
    Approval.Stage.TRANSFER_PROCUREMENT: "transfer.approve_procurement",
}
TRANSFER_JOURNEY = [
    ("Release approval", ("TR-01",)), ("Receipt approval", ("TR-02",)), ("Policy review", ("TR-03",)),
    ("Approved", ("TR-04",)), ("Handed over", ("TR-05", "TR-07")), ("Receipt confirmed", ("TR-06",)),
]


def tasks_for(request):
    """Pending approval tasks the active role may decide, never the user's own (BR-02)."""
    role = request.active_role
    stages = [stage for stage, code in Approval.STAGE_ROLES.items() if code == role.role.code]
    return (Approval.objects.filter(status=Approval.Status.PENDING, stage__in=stages)
            .filter(Q(department=role.department) | Q(department__isnull=True))
            .exclude(requested_by=request.user)
            .select_related("request", "listing__asset", "transfer__asset", "requested_by"))


@role_required(*DECIDER_ACTIONS)
def approvals(request):
    expire_overdue()
    decided = Approval.objects.filter(approver=request.user).select_related(
        "request", "listing__asset", "transfer__asset").order_by("-decided_at")[:10]
    return render(request, "transfers/approvals.html", {"tasks": tasks_for(request), "decided": decided})


@role_required(*DECIDER_ACTIONS)
def approval_detail(request, pk):
    """UI-08 Decide an approval: only the stage assigned to you."""
    approval = get_object_or_404(Approval.objects.select_related("request", "transfer__asset", "requested_by"), pk=pk)
    if approval.listing_id:
        return redirect("assets:listing", pk=approval.listing_id)
    check_action(request, STAGE_ACTION[approval.stage])
    role = request.active_role
    if approval.department_id not in (None, role.department_id):
        raise PermissionDenied("This approval belongs to another department.")
    if request.method == "POST":
        decision, reason = request.POST.get("decision"), request.POST.get("reason", "").strip()
        record, user = approval.record, request.user
        if approval.request_id:
            actions = {"approve": lambda: record.approve(user), "changes": lambda: record.request_changes(user, reason),
                       "reject": lambda: record.reject(user, reason)}
        else:
            actions = {"approve": lambda: record.approve_stage(user, approval),
                       "reject": lambda: record.reject_stage(user, reason, approval)}
        if decision in actions and perform(request, actions[decision], "Decision saved."):
            return redirect("transfers:approvals")
    record = approval.record
    return render(request, "transfers/approval_detail.html", {
        "approval": approval, "record": record, "is_request": approval.request_id is not None,
        "own": approval.requested_by_id == request.user.pk,
        "earlier": record.approvals.exclude(pk=approval.pk).order_by("created_at"),
    })


@require_POST
@role_required("hold.request")
def hold_request(request):
    """The requester asks for a hold on a published listing (classic path, without AI)."""
    request_id, listing_id = request.POST.get("request", ""), request.POST.get("listing", "")
    if not (request_id.isdigit() and listing_id.isdigit()):
        raise Http404("Unknown request or listing.")
    resource_request = get_object_or_404(ResourceRequest, pk=request_id, requester=request.user)
    listing = get_object_or_404(Listing, pk=listing_id)
    if perform(request, lambda: Reservation.request_hold(resource_request, listing, request.user),
               "Hold requested. The releasing department will confirm or decline it. Selection alone holds nothing."):
        return redirect("resource_requests:detail", pk=resource_request.pk)
    return redirect("assets:listing", pk=listing.pk)


@require_POST
@role_required("hold.confirm")
def hold_decide(request, pk):
    reservation = get_object_or_404(Reservation.objects.select_related("listing__asset", "request"), pk=pk)
    if request.active_role.department_id != reservation.listing.asset.owner_department_id:
        raise PermissionDenied("Only the releasing department can decide this hold.")
    expire_overdue()
    reservation.refresh_from_db()
    if request.POST.get("decision") == "confirm":
        perform(request, lambda: reservation.confirm(request.user), "Hold confirmed for 5 working days.")
    else:
        perform(request, lambda: reservation.decline(request.user, request.POST.get("reason", "")), "Hold declined.")
    return redirect("transfers:list")


@role_required("transfer.start")
def transfer_start(request, pk):
    expire_overdue()
    reservation = get_object_or_404(Reservation.objects.select_related("listing__asset", "request"), pk=pk,
                                    request__requester=request.user)
    existing = Transfer.objects.filter(reservation=reservation).exclude(
        status__in=[Transfer.Status.REJECTED, Transfer.Status.CANCELLED]).first()
    if existing:  # this hold has already become a transfer
        return redirect("transfers:detail", pk=existing.pk)
    form = TransferForm(request.POST or None, department=reservation.request.department, initial={
        "to_building": reservation.request.delivery_location})
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        details = {k: v for k, v in data.items() if k != "to_custodian"}
        transfer = perform(request, lambda: Transfer.start(reservation, request.user, data["to_custodian"], **details),
                           "Transfer created. It now needs the release and receipt approvals.")
        if transfer:
            return redirect("transfers:detail", pk=transfer.pk)
    return render(request, "transfers/transfer_start.html", {"form": form, "reservation": reservation})


def can_view_transfer(request, transfer):
    role = request.active_role
    if transfer.request.requester_id == request.user.pk:
        return True
    if role.role.code in (Role.Code.ASSET_CUSTODIAN, Role.Code.DEPARTMENT_REPRESENTATIVE):
        return role.department_id in (transfer.from_department_id, transfer.to_department_id)
    if role.role.code == Role.Code.REQUESTER:
        return False
    return role.allows("transfer.view")


@role_required("transfer.view", "hold.confirm")
def transfer_list(request):
    expire_overdue()
    role = request.active_role
    holds = Reservation.objects.select_related("listing__asset", "request__requester")
    transfers = Transfer.objects.select_related("asset", "from_department", "to_department")
    if role.role.code in (Role.Code.ASSET_CUSTODIAN, Role.Code.DEPARTMENT_REPRESENTATIVE):
        holds = holds.filter(listing__asset__owner_department=role.department)
        transfers = transfers.filter(Q(from_department=role.department) | Q(to_department=role.department))
    elif role.role.code == Role.Code.REQUESTER:
        holds = holds.filter(request__requester=request.user)
        transfers = transfers.filter(request__requester=request.user)
    return render(request, "transfers/transfer_list.html", {
        "holds": holds.filter(status__in=Reservation.OPEN),
        "transfers": transfers,
        "can_decide_holds": role.allows("hold.confirm"),
        "is_requester": role.role.code == Role.Code.REQUESTER,
    })


@role_required("transfer.view", "hold.confirm")
def transfer_detail(request, pk):
    transfer = get_object_or_404(Transfer.objects.select_related(
        "asset__category", "request__requester", "from_department", "to_department", "to_custodian"), pk=pk)
    if not can_view_transfer(request, transfer):
        raise PermissionDenied("You can only open transfers of your department or your own requests.")
    role, user = request.active_role, request.user
    # The policy stage is shown only when BR-06 applies to this transfer.
    stages = [s for s in TRANSFER_JOURNEY
              if s[0] != "Policy review" or transfer.needs_finance() or transfer.needs_procurement()]
    current = next((i for i, (_, codes) in enumerate(stages) if transfer.status in codes), None)
    is_custodian = role.role.code == Role.Code.ASSET_CUSTODIAN
    is_rep = role.role.code == Role.Code.DEPARTMENT_REPRESENTATIVE
    impact = getattr(transfer, "impact", None)
    return render(request, "transfers/transfer_detail.html", {
        "transfer": transfer,
        "journey": [(label, current is not None and i < current, i == current)
                    for i, (label, _) in enumerate(stages)],
        "approvals": transfer.approvals.select_related("approver", "department"),
        "can_hand_over": is_custodian and role.department_id == transfer.from_department_id
                         and transfer.status == Transfer.Status.APPROVED,
        "can_receive": is_custodian and role.department_id == transfer.to_department_id
                       and transfer.status == Transfer.Status.HANDED_OVER,
        "can_resolve": is_rep and role.department_id == transfer.to_department_id
                       and transfer.status == Transfer.Status.DISPUTED,
        "can_cancel": transfer.status in (*Transfer.WAITING, Transfer.Status.APPROVED) and (
            transfer.request.requester_id == user.pk
            or (is_rep and role.department_id in (transfer.from_department_id, transfer.to_department_id))),
        "can_confirm_saving": impact is not None and not impact.purchase_avoided_confirmed and is_rep
                              and role.department_id == transfer.to_department_id,
        "impact": impact,
        "handover_form": HandoverForm(initial={"condition": transfer.asset.condition}),
        "receipt_form": ReceiptForm(initial={"received_quantity": transfer.quantity,
                                             "received_condition": transfer.handover_condition}),
        "history": AuditLog.for_record(transfer)[:30],
    })


@require_POST
@role_required("transfer.handover")
def transfer_handover(request, pk):
    transfer = get_object_or_404(Transfer, pk=pk)
    form = HandoverForm(request.POST)
    if form.is_valid():
        perform(request, lambda: transfer.hand_over(request.user, form.cleaned_data["condition"]),
                "Handover recorded. The receiving custodian now confirms receipt.")
    return redirect("transfers:detail", pk=transfer.pk)


@require_POST
@role_required("transfer.receive")
def transfer_receive(request, pk):
    transfer = get_object_or_404(Transfer, pk=pk)
    form = ReceiptForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        if request.POST.get("outcome") == "discrepancy":
            perform(request, lambda: transfer.dispute(request.user, data["received_quantity"],
                                                      data["received_condition"], data["note"]),
                    "Difference recorded. Ownership has not changed; both representatives are told.")
        else:
            perform(request, lambda: transfer.confirm_receipt(request.user, data["received_quantity"],
                                                              data["received_condition"]),
                    "Receipt confirmed. The asset now belongs to your department.")
    return redirect("transfers:detail", pk=transfer.pk)


@require_POST
@role_required("transfer.approve_receipt")
def transfer_resolve(request, pk):
    transfer = get_object_or_404(Transfer, pk=pk)
    accept = request.POST.get("resolution") == "accept"
    perform(request, lambda: transfer.resolve_dispute(request.user, accept, request.POST.get("reason", "")),
            "Dispute resolved.")
    return redirect("transfers:detail", pk=transfer.pk)


@require_POST
@role_required("transfer.start", "transfer.approve_release", "transfer.approve_receipt")
def transfer_cancel(request, pk):
    transfer = get_object_or_404(Transfer.objects.select_related("request"), pk=pk)
    if not can_view_transfer(request, transfer):
        raise PermissionDenied("You cannot cancel this transfer.")
    perform(request, lambda: transfer.cancel(request.user, request.POST.get("reason", "")),
            "Transfer cancelled. The held units are available again.")
    return redirect("transfers:detail", pk=transfer.pk)
