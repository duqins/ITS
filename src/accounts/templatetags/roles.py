from django import template

register = template.Library()


@register.filter
def allows(user_role, action):
    """{% if active_role|allows:"history.view" %} - the same check the server makes."""
    return user_role is not None and user_role.allows(action)
