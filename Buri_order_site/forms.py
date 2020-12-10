from django import forms
from django.forms.widgets import PasswordInput


class LogInForm(forms.Form):
    login = forms.CharField(max_length=150, required=True, label="Nazwa użytkownika")
    password = forms.CharField(widget=PasswordInput, required=True, label="Hasło")