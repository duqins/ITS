from datetime import date

from django import forms
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy

from accounts.models import Role, User
from assets.models import Condition

from .models import Transfer


class TransferForm(forms.ModelForm):
    """Start a transfer from a confirmed hold: who receives it, where and how it travels."""

    to_custodian = forms.ModelChoiceField(User.objects.none(), label=gettext_lazy("Receiving custodian"))

    class Meta:
        model = Transfer
        fields = ["to_custodian", "to_building", "to_room", "delivery_arrangement", "planned_date",
                  "distance_km", "van_trips", "transfer_cost_aed"]
        # "Delivery arrangement" repeats Django's default (the field name) so that it can be translated.
        labels = {"to_building": gettext_lazy("Deliver to building"), "to_room": gettext_lazy("Room"),
                  "delivery_arrangement": gettext_lazy("Delivery arrangement"),
                  "planned_date": gettext_lazy("Planned date"), "distance_km": gettext_lazy("Distance (km)"),
                  "van_trips": gettext_lazy("Van trips"), "transfer_cost_aed": gettext_lazy("Transfer cost (AED)")}
        help_texts = {"van_trips": gettext_lazy("Used for transport emissions (van trips x km x 0.25561 kg CO2e)"),
                      "transfer_cost_aed": gettext_lazy("Subtracted from the avoided purchase value in net savings")}
        widgets = {"planned_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}

    def __init__(self, *args, department=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["to_custodian"].queryset = User.objects.filter(
            user_roles__role__code=Role.Code.ASSET_CUSTODIAN, user_roles__department=department,
            user_roles__status="active").distinct()

    def clean_planned_date(self):
        value = self.cleaned_data.get("planned_date")
        if value and value < timezone.localdate():
            raise forms.ValidationError(_("The planned date cannot be in the past."))
        return value

    def clean(self):
        data = super().clean()
        for name in ("distance_km", "van_trips", "transfer_cost_aed"):
            if data.get(name) is not None and data[name] < 0:
                self.add_error(name, _("This cannot be negative."))
        return data


class HandoverForm(forms.Form):
    condition = forms.ChoiceField(choices=Condition.choices, label=gettext_lazy("Condition at handover"))


class ReceiptForm(forms.Form):
    """UI-09 Confirm what arrived."""

    received_quantity = forms.IntegerField(min_value=0, label=gettext_lazy("Received quantity"),
                                           help_text=gettext_lazy("Cannot be more than the quantity handed over"))
    received_condition = forms.ChoiceField(choices=Condition.choices, label=gettext_lazy("Received condition"))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}),
                           label=gettext_lazy("Discrepancy reason"),
                           help_text=gettext_lazy("Needed only if the quantity or condition differs from the handover"))
