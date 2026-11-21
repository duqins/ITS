from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from accounts.models import Role, UserRole
from assets.models import Asset, Listing
from resource_requests.models import ResourceRequest
from sustainability.indicators import SustainabilityIndicators, money
from transfers.models import Approval, Reservation, Transfer, add_working_days, expire_overdue
from transfers.views import tasks_for


def card(label, number, url, icon):
    return {"label": label, "number": number, "url": url, "icon": icon}


def overdue_for(request, role):
    """Approvals waiting longer than 3 working days (TBD-5) that matter to this role, and how to describe them."""
    late = [a for a in Approval.objects.filter(status=Approval.Status.PENDING).select_related(
        "request", "transfer__request") if a.is_overdue()]
    decides = role.role.code in Approval.STAGE_ROLES.values()
    deciding = [t for t in tasks_for(request) if t.is_overdue()] if decides else None
    if deciding is not None:
        return len(deciding), _("Your approvals waiting over 3 working days"), reverse("transfers:approvals")
    if role.allows("request.submit"):
        mine = [a for a in late if (a.request and a.request.requester_id == request.user.pk)
                or (a.transfer and a.transfer.request.requester_id == request.user.pk)]
        return len(mine), _("Your requests held up by a late approval"), reverse("resource_requests:list")
    if role.role.code in (Role.Code.ASSET_CUSTODIAN, Role.Code.MAINTENANCE_STAFF):
        ours = [a for a in late if a.department_id == role.department_id or (
            a.transfer and role.department_id in (a.transfer.from_department_id, a.transfer.to_department_id))]
        return len(ours), _("Late approvals in %(department)s") % {"department": role.department}, None
    return len(late), _("Late approvals on campus"), None


def glance(request, role):
    """UI-02 'at a glance' row: the few numbers everyone should see first. Savings follow the dashboard's access
    rules (only roles with dashboard.view; a representative sees their own department), green for good and red for
    bad, always with words as well."""
    tiles = []
    if role.allows("dashboard.view"):
        today = timezone.localdate()
        own = role.role.code == Role.Code.DEPARTMENT_REPRESENTATIVE
        totals = SustainabilityIndicators(today.replace(month=1, day=1), today,
                                          role.department if own else None).totals()
        net, items = totals["net_savings_aed"], totals["items_reused"]
        where = role.department if own else _("whole campus")
        tiles += [
            {"label": _("Net savings this year (%(where)s)") % {"where": where}, "value": money(net),
             "tone": "good" if net > 0 else "bad" if net < 0 else "",
             "note": _("Saving money") if net > 0 else _("Costing money") if net < 0 else _("No savings yet"),
             "url": reverse("sustainability:dashboard")},
            {"label": _("Items reused this year (%(where)s)") % {"where": where}, "value": items,
             "tone": "good" if items else "", "note": _("Kept in use instead of bought new") if items
             else _("None yet"), "url": reverse("sustainability:dashboard")},
        ]
    count, label, url = overdue_for(request, role)
    tiles.append({"label": label, "value": count, "tone": "bad" if count else "good",
                  "note": _("Needs attention") if count else _("Nothing late"), "url": url})
    return tiles


@login_required
def home(request):
    """Role dashboard (UI-02): the work waiting for the active role."""
    expire_overdue()
    role = request.active_role
    cards = []
    if role is not None:
        code, department = role.role.code, role.department
        if role.allows("request.submit"):
            mine = ResourceRequest.objects.filter(requester=request.user)
            requests_url = reverse("resource_requests:list")
            cards += [
                card(_("Drafts to finish"), mine.filter(status="RQ-01").count(), requests_url + "?status=RQ-01", "request"),
                card(_("Waiting for department approval"), mine.filter(status="RQ-02").count(),
                     requests_url + "?status=RQ-02", "clock"),
                card(_("Open: find a match"), mine.filter(status="RQ-03").count(), requests_url + "?status=RQ-03", "match"),
                card(_("Fulfilled"), mine.filter(status="RQ-06").count(), requests_url + "?status=RQ-06", "check"),
            ]
        if code in (Role.Code.ASSET_CUSTODIAN, Role.Code.DEPARTMENT_REPRESENTATIVE):
            assets = Asset.objects.filter(owner_department=department)
            assets_url = reverse("assets:list")
            cards += [
                card(_("Assets to confirm"), assets.filter(status="AS-01").exclude(registered_by=request.user).count(),
                     assets_url + "?status=AS-01", "check"),
                card(_("Assets in storage"), assets.filter(status="AS-03").count(), assets_url + "?status=AS-03", "box"),
                card(_("Assets needing verification"), assets.filter(Asset.needing_verification()).count(),
                     assets_url + "?verification=needed", "clock"),
            ]
            if code == Role.Code.DEPARTMENT_REPRESENTATIVE:
                pending = Listing.objects.filter(asset__owner_department=department, status="LS-02").count()
                waiting = ResourceRequest.objects.filter(department=department, status="RQ-02").count()
                cards += [
                    card(_("Listings to release"), pending, reverse("transfers:approvals"), "approval"),
                    card(_("Requests to approve"), waiting, reverse("resource_requests:list") + "?status=RQ-02", "approval"),
                ]
        if any(role.allows(a) for a in ("request.approve", "transfer.approve_finance", "transfer.approve_procurement")):
            tasks = list(tasks_for(request))
            cards.insert(0, card(_("Approval tasks"), len(tasks), reverse("transfers:approvals"), "approval"))
            cards.insert(1, card(_("Overdue tasks"), sum(1 for t in tasks if t.is_overdue()),
                                 reverse("transfers:approvals"), "clock"))
        transfers_url = reverse("transfers:list")
        # UI-02: confirmed holds that end within 2 working days, so the transfer is started in time.
        soon = add_working_days(timezone.now(), 2)
        ending = Reservation.objects.filter(status="RV-02", expires_at__lte=soon)
        if role.allows("hold.confirm"):
            holds = Reservation.objects.filter(listing__asset__owner_department=department, status="RV-01").count()
            cards.append(card(_("Holds to decide"), holds, transfers_url, "clock"))
            cards.append(card(_("Holds ending soon"), ending.filter(listing__asset__owner_department=department).count(),
                              transfers_url, "clock"))
        if role.allows("transfer.handover"):
            to_send = Transfer.objects.filter(from_department=department, status="TR-04").count()
            to_receive = Transfer.objects.filter(to_department=department, status="TR-05").count()
            cards += [card(_("Transfers to hand over"), to_send, transfers_url, "arrow"),
                      card(_("Deliveries to confirm"), to_receive, transfers_url, "check")]
        if role.allows("hold.request"):
            ready = Reservation.objects.filter(request__requester=request.user, status="RV-02").count()
            cards.append(card(_("Holds ready: start the transfer"), ready, transfers_url, "transfer"))
            cards.append(card(_("Holds ending soon"), ending.filter(request__requester=request.user).count(),
                              transfers_url, "clock"))
        if role.allows("role.authorise"):
            to_decide = UserRole.objects.filter(status=UserRole.Status.REQUESTED).exclude(
                requested_by=request.user).exclude(user=request.user).count()
            cards.append(card(_("Role requests to authorise"), to_decide, reverse("accounts:administration"), "user"))
        if role.allows("role.apply"):
            to_apply = UserRole.objects.filter(status=UserRole.Status.AUTHORISED).count()
            cards.append(card(_("Authorised roles to apply"), to_apply, reverse("accounts:administration"), "user"))
        if role.allows("listing.search"):
            published = Listing.objects.filter(status="LS-03").count()
            cards.append(card(_("Published items"), published, reverse("assets:search"), "match"))
        unread = request.user.notifications.filter(read_at__isnull=True).count()
        cards.append(card(_("Unread notifications"), unread, reverse("notifications:list"), "bell"))
    return render(request, "core/home.html", {"cards": cards, "glance": glance(request, role) if role else []})
