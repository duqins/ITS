from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import ngettext
from django.views.decorators.http import require_POST

from .models import Notification


@login_required
def notification_list(request):
    notifications = request.user.notifications.all()[:50]
    return render(request, "notifications/list.html", {"notifications": notifications})


@login_required
def notification_open(request, pk):
    """Mark as read and go to the record (FR-16.4)."""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_read()
    if notification.link and url_has_allowed_host_and_scheme(notification.link, allowed_hosts={request.get_host()}):
        return redirect(notification.link)
    return redirect("notifications:list")


@login_required
@require_POST
def mark_all_read(request):
    count = request.user.notifications.filter(read_at__isnull=True).update(read_at=timezone.now())
    messages.success(request, ngettext("%(count)s notification marked as read.", "%(count)s notifications marked as read.",
                                       count) % {"count": count})
    return redirect("notifications:list")
