"""Show the saved history in the reader's language.

The history is saved in English (a fixed record). On the page, known names are shown translated:
states such as "AS-01 Draft", approval stages, roles such as "Department representative · Computing",
and the actions written by the app ("hold requested"). Anything else is shown as saved.
"""

from functools import lru_cache

from django import template
from django.conf import settings
from django.utils import translation
from django.utils.translation import pgettext, pgettext_lazy

register = template.Library()


@lru_cache(maxsize=1)
def known_names():
    """English name -> translatable name, for every state, stage, role and condition."""
    from accounts.models import Role
    from assets.models import Asset, Condition, Listing
    from resource_requests.models import ResourceRequest
    from transfers.models import Approval, Reservation, Transfer

    choices = [Role.Code, Condition, Asset.Status, Listing.Status, ResourceRequest.Status, Reservation.Status,
               Transfer.Status, Approval.Status, Approval.Stage]
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
    """An action the app wrote in the history ("hold requested"), in the reader's language."""
    return pgettext("history", value) if value else value


RECORD_KINDS = {
    "asset": pgettext_lazy("record kind", "Asset"), "listing": pgettext_lazy("record kind", "Listing"),
    "resourcerequest": pgettext_lazy("record kind", "Request"), "reservation": pgettext_lazy("record kind", "Hold"),
    "transfer": pgettext_lazy("record kind", "Transfer"), "approval": pgettext_lazy("record kind", "Approval"),
    "user": pgettext_lazy("record kind", "User"), "aisuggestion": pgettext_lazy("record kind", "AI suggestion"),
    "matchrecommendation": pgettext_lazy("record kind", "AI match"),
    "sustainabilityimpact": pgettext_lazy("record kind", "Sustainability record"),
    "page": pgettext_lazy("record kind", "Page"),
}


@register.filter
def record_kind(value):
    """The kind of record in the history ("resourcerequest" -> "Request"), in the reader's language."""
    return RECORD_KINDS.get(str(value)) or str(value).capitalize()
