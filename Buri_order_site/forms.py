from Buri_order_site.models import Address
from django import forms
from django.core.validators import EmailValidator


class ChangeUserData(forms.Form):
    username = forms.CharField(max_length=100, label="Nazwa użytkownika")
    first_name = forms.CharField(max_length=100, label="Imię")
    last_name = forms.CharField(max_length=100, label="Nazwisko")
    email = forms.EmailField(validators=[EmailValidator])


class UserAddressForm(forms.Form):
    street = forms.CharField(max_length=150, label="Ulica")
    street_number = forms.IntegerField(label="Numer ulicy", min_value=1)
    house_number = forms.IntegerField(label="Numer mieszkania", min_value=1)
