from django.core.exceptions import ValidationError


def validate_street_as_string(value):
    try:
        int(value)
        raise ValidationError("Proszę podać prawidłowy adres")
    except ValueError:
        pass
