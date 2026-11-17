"""C2 Departments and assets, C3 Publish and search."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Case, IntegerField, OuterRef, Q, Subquery, Value, When
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import content_disposition_header
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from accounts.models import Role
from accounts.permissions import role_required
from audit.models import AuditLog
from core.actions import perform

from .forms import AssetForm, ListingForm, ReasonForm, SearchForm
from .models import Asset, AssetFile, Condition, Listing

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
        raise PermissionDenied(_("You can only open the assets of your own department."))
    return asset


@role_required("asset.view")
def asset_list(request):
    role = request.active_role
    assets = visible_assets(role)
    status = request.GET.get("status", "")
    if status in Asset.Status.values:
        assets = assets.filter(status=status)
    needed = request.GET.get("verification") == "needed"
    if needed:
        assets = assets.filter(Asset.needing_verification())
    return render(request, "assets/asset_list.html", {
        "assets": assets, "statuses": Asset.Status.choices, "status": status, "verification_needed": needed,
        "can_register": role.allows("asset.register"),
        "scope": role.department if role.role.code in MANAGERS else _("all departments"),
    })


def keep_files_note(request, form):
    """Browsers never keep chosen files after an error, so say that they must be chosen again."""
    if request.FILES and form.errors:
        form.add_error(None, _("Please choose your photos and documents again after fixing the fields below."))


def save_files(request, form, asset):
    note = form.save_files(asset, request.user)
    if note:
        AuditLog.record(request.user, "files changed", asset, reason=note)


@role_required("asset.register")
def asset_register(request):
    form = AssetForm(request.POST or None, request.FILES or None, department=request.active_role.department)
    if request.method == "POST" and form.is_valid():
        asset = form.build_asset()

        def register():
            asset.register(request.user, request.active_role.department)
            save_files(request, form, asset)

        result = perform(request, register, _("Saved as a draft (AS-01). Another custodian or the department "
                                              "representative must confirm it."))
        if result:
            return redirect("assets:detail", pk=asset.pk)
    keep_files_note(request, form)
    return render(request, "assets/asset_form.html", {"form": form, "title": _("Register an asset")})


@role_required("asset.register")
def asset_edit(request, pk):
    asset = get_visible_asset(request, pk)
    if asset.status != Asset.Status.DRAFT:
        messages.error(request, _("Only a draft can be edited. A confirmed asset changes through its workflows."))
        return redirect("assets:detail", pk=asset.pk)
    form = AssetForm(request.POST or None, request.FILES or None, instance=asset)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            form.save_draft_changes()
            fields = [name for name in form.changed_data if name not in ("photos", "documents", "remove_files")]
            if fields:
                AuditLog.record(request.user, "draft edited", asset, reason=", ".join(fields))
            save_files(request, form, asset)
        messages.success(request, _("Draft saved."))
        return redirect("assets:detail", pk=asset.pk)
    keep_files_note(request, form)
    return render(request, "assets/asset_form.html", {"form": form, "title": _("Edit %(code)s") % {"code": asset.code},
                                                      "asset": asset})


def can_see_files(request, asset):
    """Who may open an asset's photos and documents: whoever may open the asset, and, once it is offered in
    search, everyone who may search (FR-08.4)."""
    role = request.active_role
    if role is None:
        return False
    if role.allows("asset.view") and (role.role.code not in MANAGERS or asset.owner_department_id == role.department_id):
        return True
    public = (Listing.Status.PUBLISHED, Listing.Status.FULLY_RESERVED, Listing.Status.CLOSED)
    return role.allows("listing.search") and asset.listings.filter(status__in=public).exists()


@login_required
def asset_file(request, pk, file_pk):
    """One photo (?size=small for the list copy) or document of an asset."""
    small = request.GET.get("size") == "small"
    files = AssetFile.objects.select_related("asset").defer("data" if small else "thumbnail")
    file = get_object_or_404(files, pk=file_pk, asset_id=pk)
    if not can_see_files(request, file.asset):
        raise PermissionDenied(_("You cannot open the files of this asset."))
    content = file.thumbnail if small and file.thumbnail is not None else file.data
    response = HttpResponse(bytes(content), content_type=file.content_type)
    # Photos open in the page; documents are downloaded rather than opened inside the app.
    response["Content-Disposition"] = content_disposition_header(file.kind == AssetFile.Kind.DOCUMENT, file.name)
    response["Cache-Control"] = "private, max-age=86400"
    return response


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
        "files": asset.files.defer("data", "thumbnail"),
        "can_edit": manages and asset.status == Asset.Status.DRAFT,
        "can_confirm": manages and role.allows("asset.confirm") and asset.status == Asset.Status.DRAFT
                       and asset.registered_by_id != request.user.pk,
        "missing": asset.missing_for_confirmation() if asset.status == Asset.Status.DRAFT else [],
        "can_verify": manages and asset.status in (Asset.Status.IN_SERVICE, Asset.Status.IN_STORAGE),
        "waiting_for_other": asset.status == Asset.Status.DRAFT and asset.registered_by_id == request.user.pk,
        "can_list": manages and role.allows("listing.prepare") and asset.is_active and asset.available_qty > 0
                    and not asset.listings.filter(status__in=Listing.OPEN).exists(),
    })


@require_POST
@role_required("asset.register")
def asset_verify(request, pk):
    """The custodian or representative checks the item again: availability and condition (FR-04.4, BR-16)."""
    asset = get_visible_asset(request, pk)
    if not asset.can_be_managed_by(request.active_role):
        raise PermissionDenied(_("Only a custodian or representative of the owning department can verify it."))
    perform(request, lambda: asset.verify(request.user), _("%(code)s verified today.") % {"code": asset.code})
    return redirect("assets:detail", pk=asset.pk)


@require_POST
@role_required("asset.confirm")
def asset_confirm(request, pk):
    asset = get_visible_asset(request, pk)
    if not asset.can_be_managed_by(request.active_role):
        raise PermissionDenied(_("Only a custodian or representative of the owning department can confirm."))
    in_use = request.POST.get("placement") == "in_use"
    perform(request, lambda: asset.confirm(request.user, in_use=in_use), _("%(code)s confirmed.") % {"code": asset.code})
    return redirect("assets:detail", pk=asset.pk)


@role_required("listing.prepare")
def listing_create(request, pk):
    asset = get_visible_asset(request, pk)
    if not asset.can_be_managed_by(request.active_role):
        raise PermissionDenied(_("Only the owning department can list this asset."))
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
        if perform(request, create, _("Listing sent to your department representative for release approval.") if sent
                   else _("Listing saved as a draft.")):
            return redirect("assets:listing", pk=listing.pk)
    return render(request, "assets/listing_form.html", {"form": form, "asset": asset})


def get_visible_listing(request, pk):
    listing = get_object_or_404(Listing.objects.select_related("asset__category", "asset__owner_department"), pk=pk)
    role = request.active_role
    owner = listing.asset.can_be_managed_by(role)
    public = listing.status in (Listing.Status.PUBLISHED, Listing.Status.FULLY_RESERVED, Listing.Status.CLOSED)
    if not (owner or public):
        raise PermissionDenied(_("Unpublished listings are visible to the owning department only (FR-08.4)."))
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
        "files": listing.asset.files.defer("data", "thumbnail"),
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
        raise PermissionDenied(_("Only the owning department can submit this listing."))
    perform(request, lambda: listing.submit_for_release(request.user),
            _("Sent to the department representative for release approval."))
    return redirect("assets:listing", pk=listing.pk)


@require_POST
@role_required("listing.publish")
def listing_decide(request, pk):
    listing, owner = get_visible_listing(request, pk)
    if not owner:
        raise PermissionDenied(_("Only the owning department representative can release this listing."))
    reason = request.POST.get("reason", "")
    if request.POST.get("decision") == "approve":
        perform(request, lambda: listing.publish(request.user), _("Listing published. Staff can now find it in search."))
    else:
        perform(request, lambda: listing.reject_release(request.user, reason),
                _("Release rejected; the listing is back to draft."))
    return redirect("assets:listing", pk=listing.pk)


@require_POST
@role_required("listing.prepare")
def listing_withdraw(request, pk):
    listing, owner = get_visible_listing(request, pk)
    if not owner:
        raise PermissionDenied(_("Only the owning department can withdraw this listing."))
    perform(request, lambda: listing.withdraw(request.user, request.POST.get("reason", "").strip()),
            _("Listing withdrawn."))
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
    first_photo = AssetFile.objects.filter(asset=OuterRef("asset_id"), kind=AssetFile.Kind.PHOTO).order_by("pk")
    results = [l for l in listings.annotate(condition_rank=rank, first_photo=Subquery(first_photo.values("pk")[:1]))
               .order_by(*order) if l.remaining_quantity() > 0]
    for listing in results:
        listing.asset.first_photo = listing.first_photo
    searched = bool(request.GET)
    return render(request, "assets/search.html", {
        "form": form, "results": results, "searched": searched,
        "can_request": request.active_role.allows("request.submit"),
    })
