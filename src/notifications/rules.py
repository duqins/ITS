"""Who is told about what (C8, FR-16). Messages go only to people who may open the record (FR-16.5)."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

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
    Notification.send(deciders, instance.record, f"New approval task: {instance.get_stage_display()} for "
                                                 f"{instance.record.code}.", link)


@receiver(post_save, sender=Reservation)
def hold_requested(sender, instance, created, **kwargs):
    if created:
        Notification.send(team(instance.listing.asset.owner_department), instance,
                          f"Hold requested on {instance.listing.asset.name} ({instance.quantity}) for "
                          f"{instance.request.code}. Confirm or decline it.", reverse("transfers:list"))


@receiver(state_changed)
def record_changed(sender, instance, from_state, to_state, actor, action, reason, **kwargs):
    """FR-16.2: state changes of requests, holds and transfers reach the requester and the teams involved."""
    if sender is ResourceRequest:
        link = reverse("resource_requests:detail", args=[instance.pk])
        messages = {
            ResourceRequest.Status.OPEN: f"Your request {instance.code} was approved. You can now find matching items.",
            ResourceRequest.Status.REJECTED: f"Your request {instance.code} was rejected: {reason}",
            ResourceRequest.Status.DRAFT: f"Changes were requested on {instance.code}: {reason}",
            ResourceRequest.Status.FULFILLED: f"Your request {instance.code} is fulfilled. The item was received.",
            ResourceRequest.Status.EXPIRED: f"Your request {instance.code} expired.",
        }
        # "Approved" only after the department decision, not when a request opens again after a hold or transfer.
        if to_state == ResourceRequest.Status.OPEN and from_state != ResourceRequest.Status.PENDING_APPROVAL:
            return
        if to_state in messages and actor != instance.requester:
            Notification.send([instance.requester], instance, messages[to_state], link)
    elif sender is Reservation:
        requester, link = instance.request.requester, reverse("resource_requests:detail", args=[instance.request_id])
        if to_state == Reservation.Status.CONFIRMED:
            Notification.send([requester], instance, f"Your hold on {instance.listing.asset.name} is confirmed until "
                                                     f"{timezone.localtime(instance.expires_at):%d %b}. Start the transfer.", link)
        elif to_state == Reservation.Status.DECLINED:
            Notification.send([requester], instance, f"Your hold on {instance.listing.asset.name} was declined: {reason}", link)
        elif to_state == Reservation.Status.EXPIRED:
            Notification.send([requester, *team(instance.listing.asset.owner_department)], instance,
                              f"The hold on {instance.listing.asset.name} expired; the units are free again.", link)
    elif sender is Transfer:
        link = reverse("transfers:detail", args=[instance.pk])
        requester = instance.request.requester
        sending, receiving = team(instance.from_department), team(instance.to_department)
        if to_state == Transfer.Status.APPROVED:
            Notification.send([requester, *holders(Role.Code.ASSET_CUSTODIAN, instance.from_department)], instance,
                              f"{instance.code} is approved. The releasing custodian can hand it over.", link)
        elif to_state == Transfer.Status.HANDED_OVER:
            Notification.send([instance.to_custodian, *holders(Role.Code.ASSET_CUSTODIAN, instance.to_department)],
                              instance, f"{instance.code} was handed over. Confirm what arrived.", link)
        elif to_state == Transfer.Status.COMPLETED:
            Notification.send([requester, *sending, *receiving], instance,
                              f"{instance.code} was received by {instance.to_department}. Ownership has changed.", link)
        elif to_state == Transfer.Status.DISPUTED:
            # FR-11.5: a difference notifies both department representatives.
            Notification.send(holders(Role.Code.DEPARTMENT_REPRESENTATIVE, instance.from_department)
                              + holders(Role.Code.DEPARTMENT_REPRESENTATIVE, instance.to_department), instance,
                              f"A difference was recorded on {instance.code}: {reason}", link)
        elif to_state in (Transfer.Status.REJECTED, Transfer.Status.CANCELLED):
            Notification.send([requester, *sending, *receiving], instance,
                              f"{instance.code} was {instance.get_status_display().lower()}: {reason}", link)
    elif sender is Listing and to_state == Listing.Status.PUBLISHED:
        Notification.send([instance.created_by], instance, f"{instance.code} is published and visible in search.",
                          reverse("assets:listing", args=[instance.pk]))
