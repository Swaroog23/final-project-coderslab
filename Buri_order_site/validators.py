from django.core.exceptions import ValidationError


def validate_as_string(value):
    try:
        int(value)
        raise ValidationError(f"Nieprawidłowa wartość: {value}")
    except ValueError:
        pass
