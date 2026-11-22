"""Pages of the AI features. A person always decides: the AI only suggests, ranks or drafts."""

import json

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _, ngettext
from django.views.decorators.http import require_POST

from accounts.models import Role
from accounts.permissions import role_required
from assets.models import Asset, Category, Condition, Listing
from audit.models import AuditLog
from core.actions import perform
from resource_requests.models import ResourceRequest
from sustainability.views import dashboard_scope

from .adapter import AIUnavailable
from .classification import ClassificationService
from .matching import MatchingService, confidence_label
from .models import AiSuggestion, MatchRecommendation, Task
from .report_drafts import ReportDraftService, scope_labels, unsupported_numbers
from .search import AISearchService


def managed_draft(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    if not asset.can_be_managed_by(request.active_role):
        raise PermissionDenied(_("Only the owning department can classify this asset."))
    return asset


@require_POST
@role_required("ai.review_classification")
def classify_asset(request, pk):
    asset = managed_draft(request, pk)
    if asset.status != Asset.Status.DRAFT:
        messages.error(request, _("AI suggestions are for draft records only."))
    else:
        try:
            ClassificationService().suggest(asset, request.user)
            messages.success(request, _("AI suggestion ready. Accept, edit or reject it."))
        except AIUnavailable as error:
            messages.warning(request, _("%(error)s Choose the category, condition and tags yourself.") % {"error": error})
    return redirect("assets:detail", pk=asset.pk)


@require_POST
@role_required("ai.review_classification")
def classification_respond(request, pk):
    suggestion = get_object_or_404(AiSuggestion, pk=pk, task=Task.CLASSIFICATION)
    asset = managed_draft(request, suggestion.asset_id)
    user, decision = request.user, request.POST.get("decision")
    latest = asset.ai_suggestions.filter(task=Task.CLASSIFICATION).first()
    if suggestion.user_response != AiSuggestion.Response.PENDING or suggestion != latest:
        # Checked on the server: an old or already decided suggestion can never be applied.
        messages.error(request, _("This suggestion was already decided or replaced by a newer one."))
        return redirect("assets:detail", pk=asset.pk)

    if decision == "accept":
        if not ClassificationService.can_prefill(suggestion):
            messages.error(request, _("Confidence is below 0.60, so this suggestion is an option only. Use Edit to "
                                      "choose the values yourself (SRS Table 4.2)."))
            return redirect("assets:detail", pk=asset.pk)
        perform(request, lambda: suggestion.accept_and_apply(user), _("Suggestion accepted."))
    elif decision == "edit":
        category = request.POST.get("category", "")
        values = {"category_id": int(category) if category.isdigit() else 0, "condition": request.POST.get("condition"),
                  "tags": [t.strip().lower() for t in request.POST.get("tags", "").split(",") if t.strip()],
                  "description": request.POST.get("description", "").strip()}
        if not Category.objects.filter(pk=values["category_id"]).exists() or values["condition"] not in Condition.values:
            messages.error(request, _("Choose a category and a condition."))
        else:
            perform(request, lambda: suggestion.correct_and_apply(user, values, request.POST.get("reason", "")),
                    _("Your corrected values were saved."))
    else:
        reason = request.POST.get("reason", "").strip()
        if not reason:
            messages.error(request, _("Give a reason for rejecting the suggestion."))
        else:
            suggestion.reject(user, reason)
            messages.success(request, _("Suggestion rejected. Nothing was changed on the asset."))
    return redirect("assets:detail", pk=asset.pk)


def visible_request(request, pk):
    obj = get_object_or_404(ResourceRequest, pk=pk)
    role = request.active_role
    if obj.requester_id == request.user.pk:
        return obj
    if role.role.code == Role.Code.DEPARTMENT_REPRESENTATIVE and role.department_id == obj.department_id:
        return obj
    raise PermissionDenied(_("You can only see matches for your own requests."))


@role_required("match.choose", "match.view")
def request_matches(request, pk):
    """UI-07 Review eligible matches."""
    obj = visible_request(request, pk)
    mine = obj.requester_id == request.user.pk
    if request.method == "POST":
        if not mine or obj.status != ResourceRequest.Status.OPEN:
            raise PermissionDenied(_("Only the requester can search matches for an open request."))
        matches, ai_used, note = MatchingService().find(obj)
        if note:
            messages.warning(request, note)
        elif matches:
            messages.success(request, ngettext("%(count)s eligible item ranked.",
                                               "%(count)s eligible items ranked.", len(matches))
                             % {"count": len(matches)})
        return redirect("ai:matches", pk=obj.pk)
    open_listing = (Listing.Status.PUBLISHED, Listing.Status.FULLY_RESERVED)
    matches = [m for m in MatchingService.latest(obj)
               if m.listing.status in open_listing or m.user_response != MatchRecommendation.Response.PENDING]
    for m in matches:
        m.confidence_text = confidence_label(m.confidence)
    return render(request, "ai/matches.html", {
        "obj": obj, "matches": matches, "mine": mine,
        "can_search": mine and obj.status == ResourceRequest.Status.OPEN,
        "can_choose": mine and obj.status == ResourceRequest.Status.OPEN and request.active_role.allows("match.choose"),
        "ai_used": bool(matches) and not matches[0].is_classic,
    })


@require_POST
@role_required("match.choose")
def choose_match(request, pk):
    match = get_object_or_404(MatchRecommendation.objects.select_related("request", "listing"), pk=pk)
    obj = match.request
    if obj.requester_id != request.user.pk:
        raise PermissionDenied(_("Only the requester can choose a match."))
    reason = request.POST.get("reason", "").strip()
    if perform(request, lambda: match.choose(request.user, reason),
               _("Hold requested from the releasing department. Choosing alone holds nothing.")):
        return redirect("resource_requests:detail", pk=obj.pk)
    return redirect("ai:matches", pk=obj.pk)


@require_POST
@role_required("match.choose")
def reject_match(request, pk):
    """The requester rejects a match as not suitable (AI feature 2: accept or reject)."""
    match = get_object_or_404(MatchRecommendation, pk=pk, user_response=MatchRecommendation.Response.PENDING)
    if match.request.requester_id != request.user.pk:
        raise PermissionDenied(_("Only the requester can reject a match."))
    match.reject(request.POST.get("reason", "").strip() or "Not suitable")
    AuditLog.record(request.user, f"AI match {match.asset.code} rejected", match.request, reason=match.override_reason)
    messages.success(request, _("%(item)s marked as not suitable.") % {"item": match.asset.name})
    return redirect("ai:matches", pk=match.request_id)


@require_POST
@role_required("listing.search")
def ai_search(request):
    """AI search: runs only when the user clicks the button (POST), so opening pages never calls the AI."""
    query = " ".join(request.POST.get("query", "").split())[:300]
    if len(query) < 3:
        messages.error(request, _("Describe what you need in a few words, then search again."))
        return redirect("assets:search")
    try:
        result = AISearchService().search(query, request.user)
    except AIUnavailable as error:
        messages.warning(request, _("%(error)s Use the keyword and filters above instead; they work without AI.")
                         % {"error": error})
        return redirect("assets:search")
    return redirect("ai:search_results", pk=result.pk)


@role_required("listing.search")
def ai_search_results(request, pk):
    """The ranked items of one AI search, with the AI's answer as JSON. Only the person who searched sees it."""
    result = get_object_or_404(AiSuggestion, pk=pk, task=Task.SEARCH, created_by=request.user)
    answer = result.suggestion
    listings = Listing.objects.filter(pk__in=[r["id"] for r in answer["results"]]).select_related(
        "asset__category", "asset__owner_department")
    by_id = {listing.pk: listing for listing in listings}
    rows = []
    for rank, hit in enumerate(answer["results"], start=1):
        listing = by_id.get(hit["id"])
        if listing is not None:
            rows.append({"rank": rank, "listing": listing, "relevance": hit["relevance"], "reason": hit["reason"],
                         "still_published": listing.status == Listing.Status.PUBLISHED})
    return render(request, "ai/search_results.html", {
        "result": result, "query": answer["query"], "rows": rows, "items_sent": answer.get("items_sent"),
        "json": json.dumps({"query": answer["query"], "results": answer["results"]}, indent=2, ensure_ascii=False),
        "can_request": request.active_role.allows("request.submit"),
    })


@require_POST
@role_required("report.review")
def report_draft(request):
    form, scope = dashboard_scope(request)
    back = reverse("sustainability:dashboard") + "?" + request.GET.urlencode()
    if scope is None:
        messages.error(request, _("Fix the filters first."))
        return redirect(back)
    period, department = scope_labels(scope)
    try:
        ReportDraftService().draft(scope.totals(), period, department, request.user)
        messages.success(request, _("AI-generated draft ready. Check it against the figures, edit it, then publish."))
    except AIUnavailable as error:
        messages.warning(request, _("%(error)s The conventional figures above are still complete.") % {"error": error})
    return redirect(back)


@require_POST
@role_required("report.review")
def report_publish(request, pk):
    suggestion = get_object_or_404(AiSuggestion, pk=pk, task=Task.REPORT, user_response=AiSuggestion.Response.PENDING)
    text = request.POST.get("summary", "").strip()
    back = request.POST.get("next", "")
    if not url_has_allowed_host_and_scheme(back, allowed_hosts={request.get_host()}):
        back = reverse("sustainability:dashboard")
    if request.POST.get("decision") == "reject":
        suggestion.reject(request.user, request.POST.get("reason", "").strip() or "Not published")
        messages.success(request, _("Draft discarded."))
        return redirect(back)
    problems = unsupported_numbers(text, suggestion.suggestion["figures"])
    if not text or problems:
        request.session[f"report_text_{suggestion.pk}"] = text  # shown again in the box (keeps the edits)
        messages.error(request, _("The summary has numbers that are not in the dashboard figures: %(numbers)s. "
                                  "Correct them before publishing.") % {"numbers": ", ".join(problems)} if problems
                       else _("The summary is empty."))
        return redirect(back)
    if text == suggestion.suggestion["summary"]:
        suggestion.accept(request.user)
    else:
        suggestion.correct(request.user, {**suggestion.suggestion, "summary": text}, "Edited before publishing")
    messages.success(request, _("Summary published with your name as reviewer."))
    return redirect(back)
