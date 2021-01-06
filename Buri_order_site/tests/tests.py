from Buri_order_site.models import Address
from django.http import response
import pytest

from django.test import TestCase
from django.contrib.auth.models import User


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