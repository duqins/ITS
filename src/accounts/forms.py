from django import forms
from django.utils.translation import gettext_lazy

from .models import User


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
