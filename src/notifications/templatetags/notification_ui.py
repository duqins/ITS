from django import template

register = template.Library()


@register.inclusion_tag("notifications/_bell.html", takes_context=True)
def notification_bell(context):
    """The unread count on every page (FR-16.4)."""
    user = context["request"].user
    return {"unread": user.notifications.filter(read_at__isnull=True).count()}
