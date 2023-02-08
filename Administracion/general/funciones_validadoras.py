from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def validar_correo(correo):
    """Dada una cadena, determina si es una dirección de correo electrónico
    válida utilizando la función validate_email() de Django."""

    try:
        validate_email(correo)
        valid_email = True

    except ValidationError:
        valid_email = False

    return valid_email
