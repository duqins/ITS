from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from accounts.models import Role, UserRole
from assets.models import Asset, Listing
from resource_requests.models import ResourceRequest
from transfers.models import Reservation, Transfer, add_working_days, expire_overdue
from transfers.views import tasks_for


def card(label, number, url, icon):
    return {"label": label, "number": number, "url": url, "icon": icon}


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
    return render(request, "core/home.html", {"cards": cards})
