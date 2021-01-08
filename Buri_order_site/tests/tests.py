from django.contrib.auth.models import User
from django.http.cookie import SimpleCookie

from Buri_order_site.models import Address, CartProduct, Product, Cart

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
def test_change_user_data(client, create_user_for_test):
    client.login(username="Test", password="hasło1234")
    new_data = {
        "first_name": "test_first",
        "last_name": "test_last",
        "email": "test@test.pl",
    }
    response = client.post(f"/user/{create_user_for_test.id}/", new_data)
    user = User.objects.get(username="Test")
    assert user.first_name == new_data["first_name"]
    assert user.last_name == new_data["last_name"]
    assert user.email == new_data["email"]


@pytest.mark.django_db
def test_change_username(client, create_user_for_test):
    client.login(username="Test", password="hasło1234")
    response = client.post(
        f"/user/{create_user_for_test.id}/change_username/", {"username": "Test1"}
    )
    assert response.status_code == 200
    assert User.objects.get(username="Test1")


@pytest.mark.django_db
def test_change_password(client, create_user_for_test):
    client.login(username="Test", password="hasło1234")
    new_data = {
        "old_password": "hasło1234",
        "new_password1": "hasło4321",
        "new_password2": "hasło4321",
    }
    response = client.post(
        f"/user/{create_user_for_test.id}/change_password/", new_data
    )
    assert response.status_code == 302
    assert response.url == "/"
    client.logout()
    assert client.login(username="Test", password="hasło4321")


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
    assert (
        Address.objects.get(street=new_address["street"]).user.id
        == create_user_for_test.id
    )


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
    assert Product.objects.get(name="test")


@pytest.mark.django_db
def test_add_to_cart(client, create_ingredient, create_category, create_user_for_test):
    client.login(username="Test", password="hasło1234")
    new_product = {
        "name": "test",
        "price": 10,
        "categories": create_category,
        "ingredients": create_ingredient,
        "details": "test",
    }
    response = client.post("/add_product/", new_product)
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


@pytest.mark.django_db
def test_add_to_cart_anonymous_user(
    client, create_user_for_test, create_ingredient, create_category
):
    client.login(username="Test", password="hasło1234")
    new_product = {
        "name": "test",
        "price": 10,
        "categories": create_category,
        "ingredients": create_ingredient,
        "details": "test",
    }
    response = client.post("/add_product/", new_product)
    client.logout()
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
        "/cart/None/",
    )
    assert response.status_code == 200
    assert (product, amount) in response.context["chosen_products"]


@pytest.mark.django_db
def test_delete_product_from_cart(
    client, create_ingredient, create_category, create_user_for_test
):
    client.login(username="Test", password="hasło1234")
    new_product = {
        "name": "test",
        "price": 10,
        "categories": create_category,
        "ingredients": create_ingredient,
        "details": "test",
    }
    response = client.post("/add_product/", new_product)
    product = Product.objects.all()[0]
    amount = 1
    cookie_value = json.dumps({f"{product.id}": f"{amount}"})
    cookie = SimpleCookie({f"product_{product.id}_and_amount": cookie_value})
    client.cookies = cookie
    response = client.post(
        f"/cart/{create_user_for_test.id}/", {"delete-btn": client.cookies}
    )
    assert response.status_code == 302
    assert response.url == f"/cart/{create_user_for_test.id}/"
    assert (
        cookie_value
        not in client.cookies.value_decode(client.cookies)[0][
            f"product_{product.id}_and_amount"
        ].value
    )


@pytest.mark.django_db
def test_delete_product_from_cart_anonymous_user(
    client, create_ingredient, create_category, create_user_for_test
):
    client.login(username="Test", password="hasło1234")
    new_product = {
        "name": "test",
        "price": 10,
        "categories": create_category,
        "ingredients": create_ingredient,
        "details": "test",
    }
    response = client.post("/add_product/", new_product)
    product = Product.objects.all()[0]
    amount = 1
    cookie_value = json.dumps({f"{product.id}": f"{amount}"})
    cookie = SimpleCookie({f"product_{product.id}_and_amount": cookie_value})
    client.cookies = cookie
    response = client.post("/cart/None/", {"delete-btn": client.cookies})
    assert response.status_code == 302
    assert response.url == "/cart/None/"
    assert (
        cookie_value
        not in client.cookies.value_decode(client.cookies)[0][
            f"product_{product.id}_and_amount"
        ].value
    )


@pytest.mark.django_db
def test_new_address_payment(
    client, create_ingredient, create_category, create_user_for_test
):
    client.login(username="Test", password="hasło1234")
    new_product = {
        "name": "test",
        "price": 10,
        "categories": create_category,
        "ingredients": create_ingredient,
        "details": "test",
    }
    response = client.post("/add_product/", new_product)
    product = Product.objects.all()[0]
    amount = 1
    cookie_value = json.dumps({f"{product.id}": f"{amount}"})
    cookie = SimpleCookie({f"product_{product.id}_and_amount": cookie_value})
    client.cookies = cookie
    assert (
        cookie_value
        in client.cookies.value_decode(client.cookies)[0][
            f"product_{product.id}_and_amount"
        ].value
    )
    response = client.get(f"/cart/{create_user_for_test.id}/")
    response = client.get(f"/cart/{create_user_for_test.id}/new_address_payment/")
    addresses_before = Address.objects.count()
    new_address = {"street": "test", "street_number": 1, "house_number": 1}
    response = client.post(
        f"/cart/{create_user_for_test.id}/new_address_payment/", new_address
    )
    assert response.status_code == 200
    assert Address.objects.count() == addresses_before + 1
    assert CartProduct.objects.count() == 1
    assert Cart.objects.count() == 1
    assert Cart.objects.all()[0].user.id == create_user_for_test.id
    assert CartProduct.objects.all()[0].cart.id == Cart.objects.all()[0].id
    assert CartProduct.objects.all()[0].product.id == product.id
    assert CartProduct.objects.all()[0].amount == amount


@pytest.mark.django_db
def test_new_address_payment_anonymous_user(
    client, create_ingredient, create_category, create_user_for_test
):
    client.login(username="Test", password="hasło1234")
    new_product = {
        "name": "test",
        "price": 10,
        "categories": create_category,
        "ingredients": create_ingredient,
        "details": "test",
    }
    response = client.post("/add_product/", new_product)
    client.logout()
    product = Product.objects.all()[0]
    amount = 1
    cookie_value = json.dumps({f"{product.id}": f"{amount}"})
    cookie = SimpleCookie({f"product_{product.id}_and_amount": cookie_value})
    client.cookies = cookie
    assert (
        cookie_value
        in client.cookies.value_decode(client.cookies)[0][
            f"product_{product.id}_and_amount"
        ].value
    )
    response = client.get(f"/cart/None/")
    response = client.get(f"/cart/None/new_address_payment/")
    addresses_before = Address.objects.count()
    new_address = {"street": "test", "street_number": 1, "house_number": 1}
    response = client.post(f"/cart/None/new_address_payment/", new_address)
    assert response.status_code == 200
    assert CartProduct.objects.count() == 1
    assert Cart.objects.count() == 1
    assert Cart.objects.all()[0].user == None
    assert CartProduct.objects.all()[0].cart.id == Cart.objects.all()[0].id
    assert CartProduct.objects.all()[0].product.id == product.id
    assert CartProduct.objects.all()[0].amount == amount


@pytest.mark.django_db
def test_old_address_payment(
    client, create_user_for_test, create_ingredient, create_category
):
    client.login(username="Test", password="hasło1234")
    new_product = {
        "name": "test",
        "price": 10,
        "categories": create_category,
        "ingredients": create_ingredient,
        "details": "test",
    }
    response = client.post("/add_product/", new_product)
    new_address = {"street": "test", "street_number": 1, "house_number": 1}
    addresses_before = Address.objects.count()
    response = client.post(
        f"/user/{create_user_for_test.id}/add_new_address/",
        new_address,
    )
    assert Address.objects.count() == addresses_before + 1
    product = Product.objects.all()[0]
    amount = 1
    cookie_value = json.dumps({f"{product.id}": f"{amount}"})
    cookie = SimpleCookie({f"product_{product.id}_and_amount": cookie_value})
    client.cookies = cookie
    assert (
        cookie_value
        in client.cookies.value_decode(client.cookies)[0][
            f"product_{product.id}_and_amount"
        ].value
    )
    client.login(username="Test", password="hasło1234")
    response = client.get(f"/cart/{create_user_for_test.id}/")
    response = client.get(f"/cart/{create_user_for_test.id}/old_address_payment/")
    response = client.post(
        f"/cart/{create_user_for_test.id}/old_address_payment/",
        {"address": (Address.objects.all()[0].id)},
    )
    assert response.status_code == 200
    assert CartProduct.objects.count() == 1
    assert Cart.objects.count() == 1
    assert Cart.objects.all()[0].user.id == create_user_for_test.id
    assert CartProduct.objects.all()[0].cart.id == Cart.objects.all()[0].id
    assert CartProduct.objects.all()[0].product.id == product.id
    assert CartProduct.objects.all()[0].amount == amount
