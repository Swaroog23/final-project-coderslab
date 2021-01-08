from Buri_order_site.models import Category, Ingredients, Product
import pytest
import sys
import os

from django.test import Client
from django.contrib.auth.models import User

sys.path.append(os.path.dirname(__file__))


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def create_user_for_test():
    test_user = User.objects.create_user(username="Test", password="hasło1234")
    test_user.is_staff = True
    test_user.save()
    return test_user


@pytest.fixture
def create_category():
    category = Category.objects.create(name="Test", details="test")
    return category


@pytest.fixture
def create_ingredient():
    ingredient = Ingredients.objects.create(
        name="Test_ing", is_gluten=True, is_not_vegan=True, is_allergic=True
    )
    return ingredient


@pytest.fixture
def create_product():
    product = Product.objects.create(
        name="test",
        price=10,
        categories=create_category(),
        ingredients=create_ingredient(),
        details="test",
    )
    return product