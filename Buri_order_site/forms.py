from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator


class ChangeUserData(forms.Form):
    username = forms.CharField(max_length=100, label="Nazwa użytkownika")
    first_name = forms.CharField(max_length=100, label="Imię")
    last_name = forms.CharField(max_length=100, label="Nazwisko")
    email = forms.EmailField(validators=[EmailValidator])