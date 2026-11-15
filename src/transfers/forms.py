from datetime import date

from django import forms
from django.utils import timezone

from accounts.models import Role, User
from assets.models import Condition

from .models import Transfer


class TransferForm(forms.ModelForm):
    """Start a transfer from a confirmed hold: who receives it, where and how it travels."""

    to_custodian = forms.ModelChoiceField(User.objects.none(), label="Receiving custodian")

    class Meta:
        model = Transfer
        fields = ["to_custodian", "to_building", "to_room", "delivery_arrangement", "planned_date",
                  "distance_km", "van_trips", "transfer_cost_aed"]
        labels = {"to_building": "Deliver to building", "to_room": "Room", "planned_date": "Planned date",
                  "distance_km": "Distance (km)", "van_trips": "Van trips", "transfer_cost_aed": "Transfer cost (AED)"}
        help_texts = {"van_trips": "Used for transport emissions (van trips x km x 0.25561 kg CO2e)",
                      "transfer_cost_aed": "Subtracted from the avoided purchase value in net savings"}
        widgets = {"planned_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}

    def __init__(self, *args, department=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["to_custodian"].queryset = User.objects.filter(
            user_roles__role__code=Role.Code.ASSET_CUSTODIAN, user_roles__department=department,
            user_roles__status="active").distinct()

    def clean_planned_date(self):
        value = self.cleaned_data.get("planned_date")
        if value and value < timezone.localdate():
            raise forms.ValidationError("The planned date cannot be in the past.")
        return value

    def clean(self):
        data = super().clean()
        for name in ("distance_km", "van_trips", "transfer_cost_aed"):
            if data.get(name) is not None and data[name] < 0:
                self.add_error(name, "This cannot be negative.")
        return data


class HandoverForm(forms.Form):
    condition = forms.ChoiceField(choices=Condition.choices, label="Condition at handover")


class ReceiptForm(forms.Form):
    """UI-09 Confirm what arrived."""

    received_quantity = forms.IntegerField(min_value=0, label="Received quantity",
                                           help_text="Cannot be more than the quantity handed over")
    received_condition = forms.ChoiceField(choices=Condition.choices, label="Received condition")
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}), label="Discrepancy reason",
                           help_text="Needed only if the quantity or condition differs from the handover")
