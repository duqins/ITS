from datetime import date

from django import forms
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy

from assets.models import Category

from .models import ResourceRequest


class RequestForm(forms.ModelForm):
    """UI-06 Submit a resource request."""

    class Meta:
        model = ResourceRequest
        fields = ["purpose", "category", "specifications", "quantity", "min_condition", "urgency",
                  "delivery_location", "required_by"]
        # The labels not set before repeat Django's default (the field name) so that they can be translated.
        labels = {"purpose": gettext_lazy("What do you need, and for what?"), "category": gettext_lazy("Category"),
                  "specifications": gettext_lazy("Specifications"), "quantity": gettext_lazy("Quantity"),
                  "min_condition": gettext_lazy("Minimum condition"), "urgency": gettext_lazy("Urgency"),
                  "delivery_location": gettext_lazy("Delivery location"), "required_by": gettext_lazy("Required by")}
        widgets = {
            "specifications": forms.Textarea(attrs={"rows": 2, "placeholder": gettext_lazy("For example: 24-inch, HDMI")}),
            "required_by": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(is_active=True)

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity < 1:
            raise forms.ValidationError(_("The quantity must be a positive whole number."))
        return quantity

    def clean_required_by(self):
        value = self.cleaned_data["required_by"]
        if value < timezone.localdate():
            raise forms.ValidationError(_("The required-by date must be today or later."))
        return value
