from Buri_order_site.models import Category, Ingredients
from Buri_order_site.validators import validate_as_string

from django import forms
from django.core.validators import EmailValidator


class ChangeUserData(forms.Form):
    username = forms.CharField(max_length=100, label="Nazwa użytkownika")
    first_name = forms.CharField(max_length=100, label="Imię")
    last_name = forms.CharField(max_length=100, label="Nazwisko")
    email = forms.EmailField(validators=[EmailValidator])


class UserAddressForm(forms.Form):
    street = forms.CharField(
        max_length=150, label="Ulica", validators=[validate_as_string]
    )
    street_number = forms.IntegerField(label="Numer ulicy", min_value=1)
    house_number = forms.IntegerField(label="Numer mieszkania", min_value=1)


class AddProductForm(forms.Form):
    name = forms.CharField(
        max_length=255, label="Nazwa produktu", validators=[validate_as_string]
    )
    price = forms.DecimalField(max_digits=6, decimal_places=2, label="Cena")
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        to_field_name="name",
        label="Kategorie produktu",
        widget=forms.CheckboxSelectMultiple,
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredients.objects.all(),
        to_field_name="name",
        label="Składniki",
    )
    details = forms.CharField(label="Opis", widget=forms.Textarea)
