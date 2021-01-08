from Buri_order_site.models import Address, Category, Product
from django.contrib.auth.models import User
from django.http.cookie import SimpleCookie

import pytest
import json


@pytest.mark.django_db
def test_create_new_user_and_login(client):
    response = client.get("/create_user/")
    assert response.status_code == 200
    user_count_before = User.objects.count()
    user_created_response = client.post(
        "/create_user/",
        {"username": "Test", "password1": "hasło1234", "password2": "hasło1234"},
    )
    assert user_created_response.status_code == 200
    assert User.objects.count() == user_count_before + 1
    assert client.login(username="Test", password="hasło1234")


@pytest.mark.django_db
def test_logout_user(client, create_user_for_test):
    assert client.login(username="Test", password="hasło1234") == True
    response = client.get("/logout/")
    assert response.status_code == 302
    assert response.url == "/"


@pytest.mark.django_db
def test_add_new_address(client, create_user_for_test):
    client.login(username="Test", password="hasło1234")
    addresses_before = Address.objects.count()
    new_address = {"street": "test", "street_number": 1, "house_number": 1}
    response = client.post(
        f"/user/{create_user_for_test.id}/add_new_address/",
        new_address,
    )
    assert response.status_code == 200
    assert Address.objects.count() == addresses_before + 1
    assert Address.objects.get(street=new_address["street"])


@pytest.mark.django_db
def test_add_product(client, create_user_for_test, create_category, create_ingredient):
    client.login(username="Test", password="hasło1234")
    products_before = Product.objects.count()
    new_product = {
        "name": "test",
        "price": 10,
        "categories": create_category,
        "ingredients": create_ingredient,
        "details": "test",
    }
    response = client.post("/add_product/", new_product)
    assert response.status_code == 200
    assert Product.objects.count() == products_before + 1


@pytest.mark.django_db
def test_delete_new_address(
    client, create_user_for_test, create_category, create_ingredient
):
    client.login(username="Test", password="hasło1234")
    new_address = {"street": "test", "street_number": 1, "house_number": 1}
    response = client.post(
        f"/user/{create_user_for_test.id}/add_new_address/",
        new_address,
    )
    assert Address.objects.count() == 1
    response = client.post(
        f"/user/{create_user_for_test.id}/delete_address/",
        {"address": (Address.objects.all()[0].id)},
    )
    assert response.status_code == 200
    assert Address.objects.count() == 0


@pytest.mark.django_db
def test_add_to_cart(client, create_product, create_category, create_user_for_test):
    client.login(username="Test", password="hasło1234")
    product = Product.objects.all()[0]
    amount = 1
    cookie = SimpleCookie(
        {f"product_{product.id}_and_amount": json.dumps({f"{product.id}": f"{amount}"})}
    )
    client.cookies = cookie
    response = client.post(f"/categories/{create_category.id}")
    assert response.status_code == 302
    assert response.url == f"/categories/{create_category.id}"
    assert client.cookies == cookie
    response = client.get(
        f"/cart/{create_user_for_test.id}/",
    )
    assert response.status_code == 200
    assert (product, amount) in response.context["chosen_products"]
