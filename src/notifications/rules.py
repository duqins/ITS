"""Who is told about what (C8, FR-16). Messages go only to people who may open the record (FR-16.5).

Each message is passed as a function, so Notification.send writes it in every recipient's own language."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from accounts.models import Role, User
from assets.models import Listing
from audit.lifecycle import state_changed
from resource_requests.models import ResourceRequest
from transfers.models import Approval, Reservation, Transfer

from .models import Notification


def holders(role_code, department=None):
    users = User.objects.filter(user_roles__role__code=role_code, user_roles__status="active", is_active=True)
    if department is not None:
        users = users.filter(user_roles__department=department)
    return list(users.distinct())


def team(department):
    """Custodians and the representative of a department."""
    return holders(Role.Code.ASSET_CUSTODIAN, department) + holders(Role.Code.DEPARTMENT_REPRESENTATIVE, department)


@receiver(post_save, sender=Approval)
def approval_task_created(sender, instance, created, **kwargs):
    """FR-16.1: tell the people who can decide a new approval task."""
    if not created:
        return
    deciders = [u for u in holders(instance.required_role, instance.department) if u != instance.requested_by]
    link = (reverse("assets:listing", args=[instance.listing_id]) if instance.listing_id
            else reverse("transfers:approval", args=[instance.pk]))
    Notification.send(deciders, instance.record, lambda: _("New approval task: %(stage)s for %(code)s.") % {
        "stage": instance.get_stage_display(), "code": instance.record.code}, link)


@receiver(post_save, sender=Reservation)
def hold_requested(sender, instance, created, **kwargs):
    if created:
        Notification.send(team(instance.listing.asset.owner_department), instance,
                          lambda: _("Hold requested on %(item)s (%(quantity)s) for %(request)s. Confirm or decline it.") % {
                              "item": instance.listing.asset.name, "quantity": instance.quantity,
                              "request": instance.request.code},
                          reverse("transfers:list"))


@receiver(state_changed)
def record_changed(sender, instance, from_state, to_state, actor, action, reason, **kwargs):
    """FR-16.2: state changes of requests, holds and transfers reach the requester and the teams involved."""
    if sender is ResourceRequest:
        link = reverse("resource_requests:detail", args=[instance.pk])
        code = instance.code
        messages = {
            ResourceRequest.Status.OPEN: lambda: _(
                "Your request %(code)s was approved. You can now find matching items.") % {"code": code},
            ResourceRequest.Status.REJECTED: lambda: _(
                "Your request %(code)s was rejected: %(reason)s") % {"code": code, "reason": reason},
            ResourceRequest.Status.DRAFT: lambda: _(
                "Changes were requested on %(code)s: %(reason)s") % {"code": code, "reason": reason},
            ResourceRequest.Status.FULFILLED: lambda: _(
                "Your request %(code)s is fulfilled. The item was received.") % {"code": code},
            ResourceRequest.Status.EXPIRED: lambda: _("Your request %(code)s expired.") % {"code": code},
        }
        # "Approved" only after the department decision, not when a request opens again after a hold or transfer.
        if to_state == ResourceRequest.Status.OPEN and from_state != ResourceRequest.Status.PENDING_APPROVAL:
            return
        if to_state in messages and actor != instance.requester:
            Notification.send([instance.requester], instance, messages[to_state], link)
    elif sender is Reservation:
        requester, link = instance.request.requester, reverse("resource_requests:detail", args=[instance.request_id])
        item = instance.listing.asset.name
        if to_state == Reservation.Status.CONFIRMED:
            # The date keeps its English format (for example "06 Nov") in every language.
            until = f"{timezone.localtime(instance.expires_at):%d %b}"
            Notification.send([requester], instance, lambda: _(
                "Your hold on %(item)s is confirmed until %(date)s. Start the transfer.") % {
                "item": item, "date": until}, link)
        elif to_state == Reservation.Status.DECLINED:
            Notification.send([requester], instance, lambda: _("Your hold on %(item)s was declined: %(reason)s") % {
                "item": item, "reason": reason}, link)
        elif to_state == Reservation.Status.EXPIRED:
            Notification.send([requester, *team(instance.listing.asset.owner_department)], instance,
                              lambda: _("The hold on %(item)s expired; the units are free again.") % {"item": item},
                              link)
    elif sender is Transfer:
        link = reverse("transfers:detail", args=[instance.pk])
        requester = instance.request.requester
        sending, receiving = team(instance.from_department), team(instance.to_department)
        code = instance.code
        if to_state == Transfer.Status.APPROVED:
            Notification.send([requester, *holders(Role.Code.ASSET_CUSTODIAN, instance.from_department)], instance,
                              lambda: _("%(code)s is approved. The releasing custodian can hand it over.") % {
                                  "code": code}, link)
        elif to_state == Transfer.Status.HANDED_OVER:
            Notification.send([instance.to_custodian, *holders(Role.Code.ASSET_CUSTODIAN, instance.to_department)],
                              instance, lambda: _("%(code)s was handed over. Confirm what arrived.") % {"code": code},
                              link)
        elif to_state == Transfer.Status.COMPLETED:
            Notification.send([requester, *sending, *receiving], instance,
                              lambda: _("%(code)s was received by %(department)s. Ownership has changed.") % {
                                  "code": code, "department": instance.to_department}, link)
        elif to_state == Transfer.Status.DISPUTED:
            # FR-11.5: a difference notifies both department representatives.
            Notification.send(holders(Role.Code.DEPARTMENT_REPRESENTATIVE, instance.from_department)
                              + holders(Role.Code.DEPARTMENT_REPRESENTATIVE, instance.to_department), instance,
                              lambda: _("A difference was recorded on %(code)s: %(reason)s") % {
                                  "code": code, "reason": reason}, link)
        elif to_state == Transfer.Status.REJECTED:
            Notification.send([requester, *sending, *receiving], instance,
                              lambda: _("%(code)s was rejected: %(reason)s") % {"code": code, "reason": reason}, link)
        elif to_state == Transfer.Status.CANCELLED:
            Notification.send([requester, *sending, *receiving], instance,
                              lambda: _("%(code)s was cancelled: %(reason)s") % {"code": code, "reason": reason}, link)
    elif sender is Listing and to_state == Listing.Status.PUBLISHED:
        Notification.send([instance.created_by], instance,
                          lambda: _("%(code)s is published and visible in search.") % {"code": instance.code},
                          reverse("assets:listing", args=[instance.pk]))
