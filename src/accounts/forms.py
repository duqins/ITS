from django import forms

from .models import User


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"autocomplete": "username", "autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))


class PreferencesForm(forms.ModelForm):
    """The Settings page: how the app looks and moves for this user."""

    class Meta:
        model = User
        fields = ["theme", "motion"]
        widgets = {"theme": forms.RadioSelect, "motion": forms.RadioSelect}
