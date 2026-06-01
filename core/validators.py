import re
from rest_framework.serializers import ValidationError


def validar_dni(value):
    if value and not re.match(r"^\d{8}$", value):
        raise ValidationError("El DNI debe tener exactamente 8 digitos numericos.")
    return value


def validar_telefono(value):
    if value and not re.match(r"^\d{9}$", value):
        raise ValidationError("El telefono debe tener exactamente 9 digitos numericos.")
    return value


def validar_monto_positivo(value):
    if value is not None and value <= 0:
        raise ValidationError("El monto debe ser mayor a cero.")
    return value


def validar_cantidad_positiva(value):
    if value is not None and value < 1:
        raise ValidationError("La cantidad debe ser al menos 1.")
    return value
