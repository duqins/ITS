"""AI panels shown on other pages: classification on the asset, matches on the request, report on the dashboard."""

import re
from datetime import datetime

from django import template
from django.utils.formats import date_format
from django.utils.translation import gettext as _, gettext_lazy

from assets.models import Category, Condition

from ..adapter import ClaudeAdapter
from ..classification import ClassificationService
from ..models import AiSuggestion, Task
from ..report_drafts import scope_labels

register = template.Library()


@register.filter
def condition_label(value):
    """A saved condition code ("not_working") as people read it, in their language."""
    return dict(Condition.choices).get(value, value)


@register.inclusion_tag("ai/_classification_panel.html", takes_context=True)
def classification_panel(context, asset):
    request = context["request"]
    role = getattr(request, "active_role", None)
    suggestion = asset.ai_suggestions.filter(task=Task.CLASSIFICATION).first()
    may_review = role is not None and role.allows("ai.review_classification") and asset.can_be_managed_by(role)
    return {
        "asset": asset,
        "suggestion": suggestion,
        "can_ask": may_review and asset.status == asset.Status.DRAFT,
        "can_decide": may_review and asset.status == asset.Status.DRAFT and suggestion is not None
                      and suggestion.user_response == AiSuggestion.Response.PENDING,
        "can_prefill": suggestion is not None and ClassificationService.can_prefill(suggestion),
        "ai_on": ClaudeAdapter.is_configured(),
        "categories": Category.objects.filter(is_active=True),
        "conditions": Condition.choices,
        "csrf_token": context.get("csrf_token"),
    }


@register.inclusion_tag("ai/_matches_link.html", takes_context=True)
def matches_link(context, resource_request):
    request = context["request"]
    return {"obj": resource_request, "show": resource_request.requester_id == request.user.pk
            and resource_request.status in ("RQ-03", "RQ-04")}


@register.inclusion_tag("ai/_report_panel.html", takes_context=True)
def report_panel(context):
    request = context["request"]
    role = getattr(request, "active_role", None)
    scope = context.get("scope")
    if scope is None:
        reports = AiSuggestion.objects.none()
    else:
        # Only a summary of exactly this period and department belongs next to these figures.
        period, department = scope_labels(scope)
        reports = AiSuggestion.objects.filter(task=Task.REPORT, suggestion__period=period,
                                              suggestion__department=department).select_related("responded_by")
    draft = reports.filter(user_response=AiSuggestion.Response.PENDING).first()
    return {
        "draft": draft,
        # The text the reviewer typed comes back after a refused publish, so their edits are not lost.
        "draft_text": request.session.pop(f"report_text_{draft.pk}", None) if draft else None,
        "published": reports.filter(user_response__in=[AiSuggestion.Response.ACCEPTED,
                                                       AiSuggestion.Response.CORRECTED]).order_by("-responded_at").first(),
        "can_review": role is not None and role.allows("report.review"),
        "ai_on": ClaudeAdapter.is_configured(),
        "query": request.GET.urlencode(),
        "path": request.get_full_path(),
        "csrf_token": context.get("csrf_token"),
    }


# A report draft is saved in English: the figures are what the AI was given and the period is the key that
# ties a summary to its dashboard. These filters show them in the reader's language.
FIGURE_NAMES = {
    "Period": gettext_lazy("Period"), "Department": gettext_lazy("Department"),
    "Completed transfers": gettext_lazy("Completed transfers"), "Items reused": gettext_lazy("Items reused"),
    "Waste diverted (kg)": gettext_lazy("Waste diverted (kg)"),
    "Confirmed avoided purchases (requests)": gettext_lazy("Confirmed avoided purchases (requests)"),
    "Avoided purchase value (AED)": gettext_lazy("Avoided purchase value (AED)"),
    "Net financial savings (AED)": gettext_lazy("Net financial savings (AED)"),
    "Carbon saved, low estimate (kg CO2e)": gettext_lazy("Carbon saved, low estimate (kg CO2e)"),
    "Carbon saved, high estimate (kg CO2e)": gettext_lazy("Carbon saved, high estimate (kg CO2e)"),
    "Reuse rate (%)": gettext_lazy("Reuse rate (%)"),
}


@register.filter
def period_text(value):
    """ "01 Jan 2026 to 06 Nov 2026" in the reader's language."""
    match = re.fullmatch(r"(\d\d \w{3} \d{4}) to (\d\d \w{3} \d{4})", str(value or ""))
    if not match:
        return value
    start, end = (datetime.strptime(day, "%d %b %Y").date() for day in match.groups())
    return _("%(start)s to %(end)s") % {"start": date_format(start), "end": date_format(end)}


@register.filter
def department_text(value):
    return _("All departments") if value == "All departments" else value


@register.filter
def figures_text(value):
    """The figures the AI was given, one per line, with the names and the period in the reader's language."""
    lines = []
    for line in str(value or "").splitlines():
        name, colon, figure = line.partition(": ")
        if name == "Period":
            figure = period_text(figure)
        elif name == "Department":
            figure = department_text(figure)
        elif figure == "N/A":
            figure = _("N/A")
        lines.append(f"{FIGURE_NAMES.get(name, name)}{colon}{figure}")
    return "\n".join(lines)


@register.filter
def check_text(value):
    """The saved figures check ("Figures check: ...") in the reader's language."""
    numbers = str(value or "").partition("numbers not in the database: ")[2]
    if numbers:
        return _("Figures check: numbers not in the database: %(numbers)s") % {"numbers": numbers}
    return _("Figures check: all numbers match the database")
