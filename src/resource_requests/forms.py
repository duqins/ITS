from datetime import date

from django import forms

from assets.models import Category

from .models import ResourceRequest


class RequestForm(forms.ModelForm):
    """UI-06 Submit a resource request."""

    class Meta:
        model = ResourceRequest
        fields = ["purpose", "category", "specifications", "quantity", "min_condition", "urgency",
                  "delivery_location", "required_by"]
        labels = {"purpose": "What do you need, and for what?", "min_condition": "Minimum condition",
                  "required_by": "Required by"}
        widgets = {
            "specifications": forms.Textarea(attrs={"rows": 2, "placeholder": "For example: 24-inch, HDMI"}),
            "required_by": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(is_active=True)

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity < 1:
            raise forms.ValidationError("The quantity must be a positive whole number.")
        return quantity

    def clean_required_by(self):
        value = self.cleaned_data["required_by"]
        if value < date.today():
            raise forms.ValidationError("The required-by date must be today or later.")
        return value
