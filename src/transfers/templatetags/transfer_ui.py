"""Small pieces of the C5 workflow shown on listing and request pages."""

from django import template

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
        open_requests = ResourceRequest.objects.filter(
            requester=request.user, status=ResourceRequest.Status.OPEN, quantity__lte=listing.remaining_quantity())
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
