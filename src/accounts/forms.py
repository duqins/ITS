from django import forms


class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"autocomplete": "username", "autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))
