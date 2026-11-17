from datetime import date

from django import forms
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy

from accounts.models import Department

from .files import MAX_DOCUMENTS, MAX_PHOTOS, read_document, read_photo
from .models import Asset, AssetFile, Category, Condition, FurnitureAsset, ITAsset, Listing

DATE = forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """A file field that takes several files at once (Django's documented pattern)."""

    def __init__(self, *args, accept="", **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"accept": accept}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single = super().clean
        if isinstance(data, (list, tuple)):
            return [single(d, initial) for d in data]
        return [single(data, initial)] if data else []


class AssetForm(forms.ModelForm):
    """UI-03 Register an asset. A draft may be saved before the category is known."""

    KINDS = [("general", gettext_lazy("General asset")), ("it", gettext_lazy("IT equipment")),
             ("furniture", gettext_lazy("Furniture"))]
    kind = forms.ChoiceField(choices=KINDS, label=gettext_lazy("Type of asset"), initial="general")
    serial_number = forms.CharField(required=False, max_length=60, label=gettext_lazy("Serial number"),
                                    help_text=gettext_lazy("IT equipment only"))
    stores_data = forms.BooleanField(required=False,
                                     label=gettext_lazy("Stores data (needs data erasure before disposal)"))
    material = forms.CharField(required=False, max_length=60, label=gettext_lazy("Material"),
                               help_text=gettext_lazy("Furniture only"))
    dimensions = forms.CharField(required=False, max_length=60, label=gettext_lazy("Dimensions"),
                                 help_text=gettext_lazy("Furniture only"))
    photos = MultipleFileField(required=False, accept="image/jpeg,image/png", label=gettext_lazy("Photos"),
                               help_text=gettext_lazy("JPG or PNG, up to 5 photos of 5 MB each"))
    documents = MultipleFileField(required=False, accept="application/pdf", label=gettext_lazy("Supporting documents"),
                                  help_text=gettext_lazy("PDF, up to 5 documents of 10 MB each"))
    # FR-04.5: shown only when a possible duplicate was found.
    not_duplicate = forms.BooleanField(required=False, label=gettext_lazy("This is a different item: save it anyway"))
    remove_files = forms.ModelMultipleChoiceField(AssetFile.objects.none(), required=False,
                                                  widget=forms.CheckboxSelectMultiple,
                                                  label=gettext_lazy("Remove files"))

    class Meta:
        model = Asset
        fields = ["name", "description", "category", "condition", "quantity", "specifications", "tags",
                  "campus", "building", "room", "value", "purchase_date", "planned_retirement_date"]
        # The other labels repeat Django's default (the field name) so that they can be translated.
        labels = {"name": gettext_lazy("Name"), "description": gettext_lazy("Description"),
                  "category": gettext_lazy("Category"), "condition": gettext_lazy("Condition"),
                  "quantity": gettext_lazy("Quantity"), "specifications": gettext_lazy("Specifications"),
                  "tags": gettext_lazy("Search tags"), "campus": gettext_lazy("Campus"),
                  "building": gettext_lazy("Building"), "room": gettext_lazy("Room"),
                  "value": gettext_lazy("Estimated value per item (AED)"),
                  "purchase_date": gettext_lazy("Purchase date"),
                  "planned_retirement_date": gettext_lazy("Planned retirement date")}
        help_texts = {"tags": gettext_lazy("Separate tags with commas, for example monitor, 24-inch"),
                      "category": gettext_lazy("You can ask the AI to suggest it after saving the draft")}
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "specifications": forms.Textarea(attrs={"rows": 2}),
            "purchase_date": DATE,
            "planned_retirement_date": DATE,
        }

    def __init__(self, *args, department=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.department = department
        self.possible_duplicate = None
        self.fields["category"].queryset = Category.objects.filter(is_active=True)
        self.fields["category"].required = False
        self.fields["category"].empty_label = gettext_lazy("Not chosen yet")
        # The browser already refuses what clean_quantity and clean_purchase_date refuse.
        self.fields["quantity"].widget.attrs["min"] = 1
        self.fields["quantity"].error_messages["min_value"] = _("The quantity must be a positive whole number.")
        self.fields["value"].widget.attrs["min"] = 0
        self.fields["purchase_date"].widget.attrs["max"] = timezone.localdate().isoformat()
        instance = self.instance
        if instance.pk and instance.files.exists():
            self.fields["remove_files"].queryset = instance.files.defer("data", "thumbnail")
        else:
            self.fields.pop("remove_files")
        if instance.pk:
            # The type is fixed once the asset exists.
            self.fields.pop("kind")
            child = self.child_of(instance)
            for name in ("serial_number", "stores_data", "material", "dimensions"):
                if child is not None and hasattr(child, name):
                    self.fields[name].initial = getattr(child, name)
                else:
                    self.fields.pop(name)

    @staticmethod
    def child_of(asset):
        for related in ("itasset", "furnitureasset"):
            try:
                return getattr(asset, related)
            except Asset.DoesNotExist:
                continue
            except AttributeError:
                continue
        return None

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity < 1:
            raise forms.ValidationError(_("The quantity must be a positive whole number."))
        return quantity

    def clean_value(self):
        value = self.cleaned_data.get("value")
        if value is not None and value < 0:
            raise forms.ValidationError(_("The value cannot be negative."))
        return value

    def clean_photos(self):
        return [read_photo(upload) for upload in self.cleaned_data["photos"]]

    def clean_documents(self):
        return [read_document(upload) for upload in self.cleaned_data["documents"]]

    def clean(self):
        data = super().clean()
        kept = {AssetFile.Kind.PHOTO: 0, AssetFile.Kind.DOCUMENT: 0}
        if self.instance.pk:
            removed = {f.pk for f in data.get("remove_files") or []}
            for kind in kept:
                kept[kind] = self.instance.files.filter(kind=kind).exclude(pk__in=removed).count()
        if kept[AssetFile.Kind.PHOTO] + len(data.get("photos") or []) > MAX_PHOTOS:
            self.add_error("photos", _("An asset can have up to 5 photos."))
        if kept[AssetFile.Kind.DOCUMENT] + len(data.get("documents") or []) > MAX_DOCUMENTS:
            self.add_error("documents", _("An asset can have up to 5 documents."))
        # FR-04.5: the same department, category, name and specifications as an existing asset is a possible
        # duplicate. It is saved only after the person confirms it is a different item.
        if not self.instance.pk and self.department is not None and data.get("name"):
            same = Asset.objects.filter(owner_department=self.department, category=data.get("category"),
                                        name__iexact=data["name"].strip(),
                                        specifications__iexact=(data.get("specifications") or "").strip()).first()
            if same is not None and not data.get("not_duplicate"):
                self.possible_duplicate = same
                self.add_error(None, _("%(code)s in your department has the same category, name and specifications. "
                                       "If this is a different item, tick the box below and save again (FR-04.5).")
                               % {"code": same.code})
        return data

    def save_files(self, asset, user):
        """Add the new photos and documents and remove the ticked ones. Returns a short note for the history."""
        added = []
        for name, large, small in self.cleaned_data.get("photos") or []:
            AssetFile.objects.create(asset=asset, kind=AssetFile.Kind.PHOTO, name=name[:150], content_type="image/jpeg",
                                     size=len(large), data=large, thumbnail=small, uploaded_by=user)
            added.append(name)
        for name, data in self.cleaned_data.get("documents") or []:
            AssetFile.objects.create(asset=asset, kind=AssetFile.Kind.DOCUMENT, name=name[:150],
                                     content_type="application/pdf", size=len(data), data=data, uploaded_by=user)
            added.append(name)
        removed = [f.name for f in self.cleaned_data.get("remove_files") or []]
        if removed:
            asset.files.filter(pk__in=[f.pk for f in self.cleaned_data["remove_files"]]).delete()
        return "; ".join(filter(None, ["+ " + ", ".join(added) if added else "", "- " + ", ".join(removed) if removed else ""]))

    def clean_purchase_date(self):
        value = self.cleaned_data.get("purchase_date")
        if value and value > timezone.localdate():
            raise forms.ValidationError(_("The purchase date cannot be in the future."))
        return value

    def build_asset(self):
        """Return an unsaved Asset, ITAsset or FurnitureAsset with the entered values."""
        data = {name: self.cleaned_data.get(name) for name in self.Meta.fields}
        kind = self.cleaned_data.get("kind", "general")
        if kind == "it":
            return ITAsset(**data, serial_number=self.cleaned_data["serial_number"],
                           stores_data=self.cleaned_data["stores_data"])
        if kind == "furniture":
            return FurnitureAsset(**data, material=self.cleaned_data["material"],
                                  dimensions=self.cleaned_data["dimensions"])
        return Asset(**data)

    def save_draft_changes(self):
        asset = self.save(commit=False)
        # A draft holds nothing yet, so every unit stays available when the quantity changes.
        asset.available_qty, asset.reserved_qty, asset.allocated_qty = asset.quantity, 0, 0
        asset.save()
        child = self.child_of(asset)
        if child is not None:
            changed = [name for name in ("serial_number", "stores_data", "material", "dimensions")
                       if name in self.cleaned_data and hasattr(child, name)]
            for name in changed:
                setattr(child, name, self.cleaned_data[name])
            # Save only the IT or furniture fields: the child still holds the old copy of the shared fields.
            child.save(update_fields=changed)
        return asset


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["quantity", "available_from", "release_reason", "restrictions"]
        labels = {"quantity": gettext_lazy("Quantity to offer"), "available_from": gettext_lazy("Available from"),
                  "release_reason": gettext_lazy("Release reason"),
                  "restrictions": gettext_lazy("Restrictions or conditions")}
        widgets = {"available_from": DATE, "restrictions": forms.Textarea(attrs={"rows": 2})}

    def __init__(self, *args, asset=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.asset = asset
        self.fields["quantity"].initial = asset.available_qty
        self.fields["quantity"].help_text = _("%(count)s available") % {"count": asset.available_qty}
        self.fields["quantity"].widget.attrs.update(min=1, max=asset.available_qty)

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity < 1 or quantity > self.asset.available_qty:
            raise forms.ValidationError(_("Offer between 1 and %(count)s units.") % {"count": self.asset.available_qty})
        return quantity

    def clean(self):
        data = super().clean()
        # One open listing per asset, so the same units never appear twice in search.
        other = self.asset.listings.filter(status__in=Listing.OPEN).exclude(pk=self.instance.pk).first()
        if other is not None:
            raise forms.ValidationError(_("This asset is already offered in %(code)s. Change or withdraw that "
                                          "listing instead.") % {"code": other.code})
        return data


class SearchForm(forms.Form):
    """C3 search: keyword plus combinable filters (FR-08)."""

    SORTS = [("newest", gettext_lazy("Newest listing")), ("condition", gettext_lazy("Best condition")),
             ("quantity", gettext_lazy("Most available"))]
    q = forms.CharField(required=False, label=gettext_lazy("Keyword"), widget=forms.TextInput(attrs={
        "placeholder": gettext_lazy("Name, description, tags or specifications")}))
    category = forms.ModelChoiceField(Category.objects.filter(is_active=True), required=False,
                                      label=gettext_lazy("Category"), empty_label=gettext_lazy("Any category"))
    condition = forms.ChoiceField(required=False, label=gettext_lazy("Minimum condition"),
                                  choices=[("", gettext_lazy("Any condition"))] + list(Condition.choices))
    department = forms.ModelChoiceField(Department.objects.filter(is_active=True), required=False,
                                        label=gettext_lazy("Department"), empty_label=gettext_lazy("Any department"))
    sort = forms.ChoiceField(choices=SORTS, required=False, initial="newest", label=gettext_lazy("Sort"))


class ReasonForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), required=False)
