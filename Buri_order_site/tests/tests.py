import pytest

from django.test import TestCase
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_new_user_and_login(client):
    response = client.get("/create_user/")
    assert response.status_code == 200
    user_count_before = User.objects.count()
    user_create = client.post(
        "/create_user/",
        {"username": "Test", "password1": "hasło1234", "password2": "hasło1234"},
    )
    assert user_create.status_code == 200
    assert User.objects.count() == user_count_before + 1
    logged_client = client.login(username="Test", password="hasło1234")
    assert logged_client == True


def test_logout_user(client):
    response = client.get("/logout/")
    assert response.status_code == 302