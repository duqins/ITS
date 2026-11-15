"""C2 Departments and assets, C3 Publish and search."""

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Case, IntegerField, Q, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import Role
from accounts.permissions import role_required
from audit.models import AuditLog
from core.actions import perform

from .forms import AssetForm, ListingForm, ReasonForm, SearchForm
from .models import Asset, Condition, Listing

MANAGERS = (Role.Code.ASSET_CUSTODIAN, Role.Code.DEPARTMENT_REPRESENTATIVE)


def visible_assets(user_role):
    """Custodians and representatives see their own department's assets; reviewers see all (section 6)."""
    assets = Asset.objects.select_related("category", "owner_department", "custodian")
    if user_role.role.code in MANAGERS:
        assets = assets.filter(owner_department=user_role.department)
    return assets


def get_visible_asset(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    role = request.active_role
    if role.role.code in MANAGERS and asset.owner_department_id != role.department_id:
        raise PermissionDenied("You can only open the assets of your own department.")
    return asset


@role_required("asset.view")
def asset_list(request):
    role = request.active_role
    assets = visible_assets(role)
    status = request.GET.get("status", "")
    if status in Asset.Status.values:
        assets = assets.filter(status=status)
    return render(request, "assets/asset_list.html", {
        "assets": assets, "statuses": Asset.Status.choices, "status": status,
        "can_register": role.allows("asset.register"),
        "scope": role.department if role.role.code in MANAGERS else "all departments",
    })


@role_required("asset.register")
def asset_register(request):
    form = AssetForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        asset = form.build_asset()
        result = perform(request, lambda: asset.register(request.user, request.active_role.department),
                         "Saved as a draft (AS-01). Another custodian or the department representative must confirm it.")
        if result:
            return redirect("assets:detail", pk=asset.pk)
    return render(request, "assets/asset_form.html", {"form": form, "title": "Register an asset"})


@role_required("asset.register")
def asset_edit(request, pk):
    asset = get_visible_asset(request, pk)
    if asset.status != Asset.Status.DRAFT:
        messages.error(request, "Only a draft can be edited. A confirmed asset changes through its workflows.")
        return redirect("assets:detail", pk=asset.pk)
    form = AssetForm(request.POST or None, instance=asset)
    if request.method == "POST" and form.is_valid():
        form.save_draft_changes()
        AuditLog.record(request.user, "draft edited", asset, reason=", ".join(form.changed_data))
        messages.success(request, "Draft saved.")
        return redirect("assets:detail", pk=asset.pk)
    return render(request, "assets/asset_form.html", {"form": form, "title": f"Edit {asset.code}", "asset": asset})


@role_required("asset.view")
def asset_detail(request, pk):
    asset = get_visible_asset(request, pk)
    role = request.active_role
    manages = asset.can_be_managed_by(role)
    child = AssetForm.child_of(asset)
    return render(request, "assets/asset_detail.html", {
        "asset": asset,
        "child": child,
        "kind": {"ITAsset": "it", "FurnitureAsset": "furniture"}.get(type(child).__name__, "general"),
        "listings": asset.listings.all(),
        "can_edit": manages and asset.status == Asset.Status.DRAFT,
        "can_confirm": manages and role.allows("asset.confirm") and asset.status == Asset.Status.DRAFT
                       and asset.registered_by_id != request.user.pk,
        "waiting_for_other": asset.status == Asset.Status.DRAFT and asset.registered_by_id == request.user.pk,
        "can_list": manages and role.allows("listing.prepare") and asset.is_active and asset.available_qty > 0
                    and not asset.listings.filter(status__in=Listing.OPEN).exists(),
    })


@require_POST
@role_required("asset.confirm")
def asset_confirm(request, pk):
    asset = get_visible_asset(request, pk)
    if not asset.can_be_managed_by(request.active_role):
        raise PermissionDenied("Only a custodian or representative of the owning department can confirm.")
    in_use = request.POST.get("placement") == "in_use"
    perform(request, lambda: asset.confirm(request.user, in_use=in_use), f"{asset.code} confirmed.")
    return redirect("assets:detail", pk=asset.pk)


@role_required("listing.prepare")
def listing_create(request, pk):
    asset = get_visible_asset(request, pk)
    if not asset.can_be_managed_by(request.active_role):
        raise PermissionDenied("Only the owning department can list this asset.")
    form = ListingForm(request.POST or None, asset=asset)
    if request.method == "POST" and form.is_valid():
        listing = form.save(commit=False)
        listing.asset = asset
        listing.created_by = request.user

        def create():
            listing.save()
            if request.POST.get("submit_for") == "release":
                listing.submit_for_release(request.user)

        sent = request.POST.get("submit_for") == "release"
        if perform(request, create, "Listing sent to your department representative for release approval." if sent
                   else "Listing saved as a draft."):
            return redirect("assets:listing", pk=listing.pk)
    return render(request, "assets/listing_form.html", {"form": form, "asset": asset})


def get_visible_listing(request, pk):
    listing = get_object_or_404(Listing.objects.select_related("asset__category", "asset__owner_department"), pk=pk)
    role = request.active_role
    owner = listing.asset.can_be_managed_by(role)
    public = listing.status in (Listing.Status.PUBLISHED, Listing.Status.FULLY_RESERVED, Listing.Status.CLOSED)
    if not (owner or public):
        raise PermissionDenied("Unpublished listings are visible to the owning department only (FR-08.4).")
    return listing, owner


@role_required("listing.search")
def listing_detail(request, pk):
    listing, owner = get_visible_listing(request, pk)
    role = request.active_role
    is_owner_rep = owner and role.role.code == Role.Code.DEPARTMENT_REPRESENTATIVE
    pending = listing.pending_approval()
    return render(request, "assets/listing_detail.html", {
        "listing": listing,
        "asset": listing.asset,
        "owner": owner,
        "pending": pending,
        "can_submit": owner and role.allows("listing.prepare") and listing.status == Listing.Status.DRAFT,
        "can_decide": is_owner_rep and pending is not None and pending.requested_by_id != request.user.pk,
        "own_listing": pending is not None and pending.requested_by_id == request.user.pk,
        "can_withdraw": owner and role.allows("listing.prepare") and listing.status in (
            Listing.Status.DRAFT, Listing.Status.PENDING_RELEASE, Listing.Status.PUBLISHED),
        "reason_form": ReasonForm(),
    })


@require_POST
@role_required("listing.prepare")
def listing_submit(request, pk):
    listing, owner = get_visible_listing(request, pk)
    if not owner:
        raise PermissionDenied("Only the owning department can submit this listing.")
    perform(request, lambda: listing.submit_for_release(request.user),
            "Sent to the department representative for release approval.")
    return redirect("assets:listing", pk=listing.pk)


@require_POST
@role_required("listing.publish")
def listing_decide(request, pk):
    listing, owner = get_visible_listing(request, pk)
    if not owner:
        raise PermissionDenied("Only the owning department representative can release this listing.")
    reason = request.POST.get("reason", "")
    if request.POST.get("decision") == "approve":
        perform(request, lambda: listing.publish(request.user), "Listing published. Staff can now find it in search.")
    else:
        perform(request, lambda: listing.reject_release(request.user, reason), "Release rejected; the listing is back to draft.")
    return redirect("assets:listing", pk=listing.pk)


@require_POST
@role_required("listing.prepare")
def listing_withdraw(request, pk):
    listing, owner = get_visible_listing(request, pk)
    if not owner:
        raise PermissionDenied("Only the owning department can withdraw this listing.")
    perform(request, lambda: listing.withdraw(request.user, request.POST.get("reason", "").strip()), "Listing withdrawn.")
    return redirect("assets:listing", pk=listing.pk)


@role_required("listing.search")
def search(request):
    """Search published surplus items by keyword, category, condition and department (C3, FR-08)."""
    form = SearchForm(request.GET or None)
    listings = Listing.objects.filter(status=Listing.Status.PUBLISHED).select_related(
        "asset__category", "asset__owner_department")
    if form.is_valid():
        data = form.cleaned_data
        for word in data["q"].split():
            listings = listings.filter(
                Q(asset__name__icontains=word) | Q(asset__description__icontains=word)
                | Q(asset__tags__icontains=word) | Q(asset__specifications__icontains=word)
                | Q(asset__category__name__icontains=word) | Q(asset__category__subcategory__icontains=word)
            )
        if data["category"]:
            listings = listings.filter(asset__category=data["category"])
        if data["condition"]:
            better = [c for c in Condition.values if Condition.rank(c) >= Condition.rank(data["condition"])]
            listings = listings.filter(asset__condition__in=better)
        if data["department"]:
            listings = listings.filter(asset__owner_department=data["department"])
        sort = data["sort"] or "newest"
    else:
        sort = "newest"
    rank = Case(*[When(asset__condition=c, then=Value(Condition.rank(c))) for c in Condition.values],
                output_field=IntegerField())
    order = {"newest": ["-published_at"], "condition": ["-condition_rank", "-published_at"],
             "quantity": ["-asset__available_qty", "-published_at"]}[sort]
    results = [l for l in listings.annotate(condition_rank=rank).order_by(*order) if l.remaining_quantity() > 0]
    searched = bool(request.GET)
    return render(request, "assets/search.html", {
        "form": form, "results": results, "searched": searched,
        "can_request": request.active_role.allows("request.submit"),
    })
