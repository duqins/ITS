"""Show the saved history in the reader's language.

The history is saved in English (a fixed record). On the page, known names are shown translated:
states such as "AS-01 Draft", approval stages, roles such as "Department representative · Computing",
and the actions written by the app ("hold requested"). Anything else is shown as saved.
"""

import re
from functools import lru_cache

from django import template
from django.conf import settings
from django.utils import translation
from django.utils.translation import npgettext, pgettext, pgettext_lazy

register = template.Library()


@lru_cache(maxsize=1)
def known_names():
    """English name -> translatable name, for every state, stage, role and condition."""
    from accounts.models import Role, UserRole
    from assets.models import Asset, Condition, Listing
    from resource_requests.models import ResourceRequest
    from transfers.models import Approval, Reservation, Transfer

    choices = [Role.Code, Condition, Asset.Status, Listing.Status, ResourceRequest.Status, Reservation.Status,
               Transfer.Status, Approval.Status, Approval.Stage, UserRole.Status]
    names = {}
    with translation.override(settings.LANGUAGE_CODE):
        for kind in choices:
            for _value, label in kind.choices:
                names[str(label)] = label
    return names


@register.filter
def localized(value):
    """A saved state, stage or role in the reader's language."""
    text = str(value or "")
    names = known_names()
    if text in names:
        return names[text]
    code, space, rest = text.partition(" ")  # "AS-01 Draft"
    if space and rest in names:
        return f"{code} {names[rest]}"
    role, dot, department = text.partition(" · ")  # "Department representative · Computing"
    if dot and role in names:
        return f"{names[role]}{dot}{department}"
    return text


@register.filter
def action_text(value):
    """An action the app wrote in the history ("hold requested"), in the reader's language.

    A few actions carry a code, a number or another action inside them ("1 unit moved to AST-0007",
    "blocked: request hold"). Those are matched here, so the value is kept and only the words change.
    """
    if not value:
        return value
    moved = re.fullmatch(r"(\d+) unit(?:s|\(s\))? moved to (\S+)", value)
    if moved:
        count = int(moved[1])
        return npgettext("history", "%(count)s unit moved to %(code)s", "%(count)s units moved to %(code)s",
                         count) % {"count": count, "code": moved[2]}
    received = re.fullmatch(r"received from (\S+) by (\S+)", value)
    if received:
        return pgettext("history", "received from %(asset)s by %(transfer)s") % {
            "asset": received[1], "transfer": received[2]}
    rejected = re.fullmatch(r"AI match (\S+) rejected", value)
    if rejected:
        return pgettext("history", "AI match %(code)s rejected") % {"code": rejected[1]}
    suggestion = re.fullmatch(r"AI (\w+) suggestion (\w+)", value)
    if suggestion:
        from ai.models import AiSuggestion, Task
        task = dict(Task.choices).get(suggestion[1], suggestion[1])
        response = dict(AiSuggestion.Response.choices).get(suggestion[2], suggestion[2])
        return pgettext("history", "AI %(task)s suggestion %(response)s") % {
            "task": str(task).lower(), "response": str(response).lower()}
    blocked = re.fullmatch(r"blocked: (.+)", value)
    if blocked:
        return pgettext("history", "blocked: %(action)s") % {"action": pgettext("history", blocked[1])}
    return pgettext("history", value)


RECORD_KINDS = {
    "asset": pgettext_lazy("record kind", "Asset"), "listing": pgettext_lazy("record kind", "Listing"),
    "resourcerequest": pgettext_lazy("record kind", "Request"), "reservation": pgettext_lazy("record kind", "Hold"),
    "transfer": pgettext_lazy("record kind", "Transfer"), "approval": pgettext_lazy("record kind", "Approval"),
    "user": pgettext_lazy("record kind", "User"), "aisuggestion": pgettext_lazy("record kind", "AI suggestion"),
    "matchrecommendation": pgettext_lazy("record kind", "AI match"),
    "sustainabilityimpact": pgettext_lazy("record kind", "Sustainability record"),
    "page": pgettext_lazy("record kind", "Page"),
    "userrole": pgettext_lazy("record kind", "Role assignment"),
}


@register.filter
def record_kind(value):
    """The kind of record in the history ("resourcerequest" -> "Request"), in the reader's language."""
    return RECORD_KINDS.get(str(value)) or str(value).capitalize()


CODES = {"asset": "AST", "listing": "LST", "resourcerequest": "REQ", "reservation": "HLD", "transfer": "TRF"}


@register.filter
def record_label(entry):
    """The record of a history line as people know it: AST-0002, TRF-0002, or "Approval 12" for the rest."""
    prefix = CODES.get(entry.record_type)
    if prefix:
        return f"{prefix}-{entry.record_id:04d}"
    return f"{record_kind(entry.record_type)} {entry.record_id}"
