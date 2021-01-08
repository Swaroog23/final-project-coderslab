from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_as_string(value):
    try:
        int(value)
        raise ValidationError(f"Nieprawidłowa wartość: {value}")
    except ValueError:
        pass


def validate_as_int(value):
    if not isinstance(value, int):
        raise ValidationError(f"Nieprawidłowa wartość: {value}")


def validate_username_is_unique(value):
    try:
        User.objects.get(username=value)
        raise ValidationError("Nazwa użytkownika jest zajęta!")
    except User.DoesNotExist:
        pass
