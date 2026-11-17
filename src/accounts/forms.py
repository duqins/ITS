from django import forms
from django.utils.translation import gettext_lazy

from .models import Department, Role, User


class RoleRequestForm(forms.Form):
    """UI-14: a Business administrator asks for a role for a staff account (UC-01 step 1)."""

    user = forms.ModelChoiceField(User.objects.filter(is_active=True).order_by("first_name", "last_name"),
                                  label=gettext_lazy("Staff account"), empty_label=gettext_lazy("Choose a person"))
    role = forms.ModelChoiceField(Role.objects.all(), label=gettext_lazy("Role"), empty_label=gettext_lazy("Choose a role"))
    department = forms.ModelChoiceField(Department.objects.filter(is_active=True), label=gettext_lazy("Department"),
                                        empty_label=gettext_lazy("Choose a department"))


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, label=gettext_lazy("Username"),
                               widget=forms.TextInput(attrs={"autocomplete": "username", "autofocus": True}))
    password = forms.CharField(label=gettext_lazy("Password"),
                               widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))


class PreferencesForm(forms.ModelForm):
    """The Settings page: how the app looks and moves for this user."""

    class Meta:
        model = User
        fields = ["theme", "language", "motion"]
        widgets = {"theme": forms.RadioSelect, "language": forms.RadioSelect, "motion": forms.RadioSelect}
