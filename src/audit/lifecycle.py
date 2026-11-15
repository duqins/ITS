"""The state rules of design section 10.2 (C6).

Each record class lists its allowed moves in TRANSITIONS. change_state() is the only
way the code changes a status: it refuses any other move, writes the audit entry and
tells the rest of the app (for example notifications) through the state_changed signal.
"""

from django.dispatch import Signal

from .models import AuditLog

# Sent after every saved state change: instance, from_state, to_state, actor, action, reason.
state_changed = Signal()


class TransitionNotAllowed(Exception):
    def __init__(self, obj, from_state, to_state, action):
        self.obj = obj
        self.action = action
        label = dict(type(obj).Status.choices)
        super().__init__(
            f"{action} is not allowed: {obj._meta.verbose_name} cannot move from "
            f"{label.get(from_state, from_state)} to {label.get(to_state, to_state)}."
        )


class BusinessRuleError(Exception):
    """A rule such as no self-approval or the quantity limit was broken."""

    def __init__(self, message, obj=None, action=""):
        self.obj = obj
        self.action = action
        super().__init__(message)


def status_label(obj, code):
    return f"{code} {dict(type(obj).Status.choices).get(code, '')}".strip()


def change_state(obj, to_state, actor, action, reason="", extra_fields=()):
    from_state = obj.status
    if to_state not in obj.TRANSITIONS.get(from_state, ()):
        raise TransitionNotAllowed(obj, from_state, to_state, action)
    fields = ["status", *extra_fields]
    if hasattr(obj, "previous_status"):
        obj.previous_status = from_state
        fields.append("previous_status")
    if hasattr(obj, "version"):
        obj.version += 1
        fields.append("version")
    obj.status = to_state
    obj.save(update_fields=fields) if obj.pk else obj.save()
    AuditLog.record(actor, action, obj, before=status_label(obj, from_state), after=status_label(obj, to_state), reason=reason)
    state_changed.send(
        sender=type(obj), instance=obj, from_state=from_state, to_state=to_state,
        actor=actor, action=action, reason=reason,
    )


def record_blocked(actor, error):
    """Log a refused action (FR-02.3, design 4b). Called after the failed transaction rolled back."""
    obj = getattr(error, "obj", None)
    if obj is None or obj.pk is None:
        return
    AuditLog.record(actor, f"blocked: {getattr(error, 'action', '') or 'action'}", obj, reason=str(error))
