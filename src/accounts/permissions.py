"""Server-side permission checks (C1, design section 6).

A user acts through one active role at a time. Every view states which action it needs,
and the server refuses the request when the active role does not allow it, even if
someone types the address by hand. Refused attempts are written to the audit log.
"""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from audit.models import AuditLog

from .models import Role


def roles_allowed(action):
    return [Role.Code(code).label for code, actions in Role.ACTIONS.items() if action in actions]


def log_refusal(request, action):
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        role=str(getattr(request, "active_role", "") or ""),
        action=f"blocked: {action}",
        record_type="page",
        record_id=0,
        reason=request.path,
    )


def check_action(request, action):
    """Raise PermissionDenied unless the active role allows the action."""
    user_role = getattr(request, "active_role", None)
    if user_role is None or not user_role.allows(action):
        log_refusal(request, action)
        needed = ", ".join(roles_allowed(action)) or "an administrator"
        raise PermissionDenied(f"This needs one of these roles: {needed}. Switch role if you hold one.")
    return user_role


def role_required(*actions):
    """View decorator: the active role must allow at least one of the actions."""

    def decorator(view):
        @wraps(view)
        @login_required
        def wrapper(request, *args, **kwargs):
            user_role = getattr(request, "active_role", None)
            if user_role is None or not any(user_role.allows(a) for a in actions):
                check_action(request, actions[0])
            return view(request, *args, **kwargs)

        return wrapper

    return decorator
