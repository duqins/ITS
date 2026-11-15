"""Run one user action safely: all of it or none of it, with a clear message either way."""

from django.contrib import messages
from django.db import transaction

from audit.lifecycle import BusinessRuleError, TransitionNotAllowed, record_blocked


def perform(request, action, success_message):
    """Call action() in one database transaction.

    If a business rule or state rule refuses it, nothing is saved, the refusal is written
    to the audit log and the user sees why. Returns the action's result, or None if refused.
    """
    try:
        with transaction.atomic():
            result = action()
    except (BusinessRuleError, TransitionNotAllowed) as error:
        record_blocked(request.user, error)
        messages.error(request, str(error))
        return None
    messages.success(request, success_message)
    return True if result is None else result
