from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from accounts.models import Role
from assets.models import Asset, Listing
from resource_requests.models import ResourceRequest


def card(label, number, url, icon):
    return {"label": label, "number": number, "url": url, "icon": icon}


@login_required
def home(request):
    """Role dashboard (UI-02): the work waiting for the active role."""
    role = request.active_role
    cards = []
    if role is not None:
        code, department = role.role.code, role.department
        if role.allows("request.submit"):
            mine = ResourceRequest.objects.filter(requester=request.user)
            requests_url = reverse("resource_requests:list")
            cards += [
                card("Drafts to finish", mine.filter(status="RQ-01").count(), requests_url + "?status=RQ-01", "request"),
                card("Waiting for department approval", mine.filter(status="RQ-02").count(), requests_url + "?status=RQ-02", "clock"),
                card("Open: find a match", mine.filter(status="RQ-03").count(), requests_url + "?status=RQ-03", "match"),
                card("Fulfilled", mine.filter(status="RQ-06").count(), requests_url + "?status=RQ-06", "check"),
            ]
        if code in (Role.Code.ASSET_CUSTODIAN, Role.Code.DEPARTMENT_REPRESENTATIVE):
            assets = Asset.objects.filter(owner_department=department)
            assets_url = reverse("assets:list")
            cards += [
                card("Assets to confirm", assets.filter(status="AS-01").exclude(registered_by=request.user).count(),
                     assets_url + "?status=AS-01", "check"),
                card("Assets in storage", assets.filter(status="AS-03").count(), assets_url + "?status=AS-03", "box"),
            ]
            if code == Role.Code.DEPARTMENT_REPRESENTATIVE:
                pending = Listing.objects.filter(asset__owner_department=department, status="LS-02").count()
                waiting = ResourceRequest.objects.filter(department=department, status="RQ-02").count()
                cards += [
                    card("Listings to release", pending, assets_url, "approval"),
                    card("Requests to approve", waiting, reverse("resource_requests:list") + "?status=RQ-02", "approval"),
                ]
        if role.allows("listing.search"):
            published = Listing.objects.filter(status="LS-03").count()
            cards.append(card("Published items", published, reverse("assets:search"), "match"))
    return render(request, "core/home.html", {"cards": cards})
