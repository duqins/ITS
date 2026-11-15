"""AI panels shown on other pages: classification on the asset, matches on the request, report on the dashboard."""

from django import template

from assets.models import Category, Condition

from ..adapter import ClaudeAdapter
from ..classification import ClassificationService
from ..models import AiSuggestion, Task
from ..report_drafts import scope_labels

register = template.Library()


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
    return {
        "draft": reports.filter(user_response=AiSuggestion.Response.PENDING).first(),
        "published": reports.filter(user_response__in=[AiSuggestion.Response.ACCEPTED,
                                                       AiSuggestion.Response.CORRECTED]).order_by("-responded_at").first(),
        "can_review": role is not None and role.allows("report.review"),
        "ai_on": ClaudeAdapter.is_configured(),
        "query": request.GET.urlencode(),
        "path": request.get_full_path(),
        "csrf_token": context.get("csrf_token"),
    }
