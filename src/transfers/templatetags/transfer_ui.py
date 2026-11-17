"""Small pieces of the C5 workflow shown on listing and request pages."""

from django import template
from django.utils.translation import gettext as _

from accounts.models import Role
from resource_requests.models import ResourceRequest

from ..models import Reservation, Transfer

register = template.Library()


@register.inclusion_tag("transfers/_hold_form.html", takes_context=True)
def hold_form(context, listing):
    """Lets a requester ask for a hold on this listing for one of their approved, open requests."""
    request = context["request"]
    role = getattr(request, "active_role", None)
    open_requests = []
    if role is not None and role.allows("hold.request") and listing.status == listing.Status.PUBLISHED:
        candidates = ResourceRequest.objects.filter(
            requester=request.user, status=ResourceRequest.Status.OPEN, quantity__lte=listing.remaining_quantity()
        ).exclude(department=listing.asset.owner_department_id)
        # Only requests this item can serve: same category, good enough condition, available in time (BR-14).
        open_requests = [r for r in candidates if r.listing_problem(listing) is None]
    return {"listing": listing, "open_requests": open_requests, "csrf_token": context.get("csrf_token")}


@register.simple_tag(takes_context=True)
def approval_task(context, record):
    """The pending approval on this request or transfer that the viewer's active role may decide, if any."""
    from ..views import tasks_for

    request = context["request"]
    if getattr(request, "active_role", None) is None:
        return None
    field = "transfer" if isinstance(record, Transfer) else "request"
    return tasks_for(request).filter(**{field: record}).first()


@register.inclusion_tag("transfers/_request_progress.html", takes_context=True)
def request_progress(context, resource_request):
    return {
        "holds": Reservation.objects.filter(request=resource_request).select_related("listing__asset"),
        "transfers": Transfer.objects.filter(request=resource_request),
        "mine": resource_request.requester_id == context["request"].user.pk,
    }


@register.simple_tag(takes_context=True)
def next_step(context, record):
    """Who acts next on this request or transfer, in one sentence (FR-07.5). Empty when nothing is waiting."""
    if isinstance(record, Transfer):
        sender, receiver = record.from_department, record.to_department
        steps = {
            "TR-01": lambda: _("The %(department)s representative approves the release.") % {"department": sender},
            "TR-02": lambda: _("The %(department)s representative approves the receipt.") % {"department": receiver},
            "TR-03": lambda: _("Finance or Procurement reviews the transfer (BR-06)."),
            "TR-04": lambda: _("A %(department)s custodian hands the item over.") % {"department": sender},
            "TR-05": lambda: _("%(custodian)s confirms what arrived. Until then the item still belongs to "
                               "%(department)s (BR-13).") % {"custodian": record.to_custodian, "department": sender},
            "TR-07": lambda: _("The %(department)s representative decides what happens with the difference.") % {
                "department": receiver},
        }
        return steps[record.status]() if record.status in steps else ""
    user = context["request"].user
    mine = record.requester_id == user.pk
    steps = {
        "RQ-01": lambda: _("Submit it for department approval."),
        "RQ-02": lambda: _("The %(department)s department representative approves it.") % {
            "department": record.department},
        "RQ-03": lambda: _("Find a matching item and ask the releasing department for a hold.") if mine else
                         _("%(requester)s finds a matching item and asks the releasing department for a hold.") % {
                             "requester": record.requester},
        "RQ-04": lambda: _("The releasing department confirms or declines the hold."),
        "RQ-05": lambda: _("The transfer is approved, handed over and received."),
    }
    text = steps[record.status]() if record.status in steps else ""
    if (record.status == "RQ-02" and mine
            and user.has_role(Role.Code.DEPARTMENT_REPRESENTATIVE, record.department)):
        text += " " + _("You made this request, so another representative must decide it (BR-02).")
    return text
