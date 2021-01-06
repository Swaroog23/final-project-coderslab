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
    User.objects.create_user(username="Test", password="hasło1234")
