from django.test import TestCase
from rest_framework.serializers import ValidationError
from core.validators import (
    validar_dni, validar_telefono,
    validar_monto_positivo, validar_cantidad_positiva
)


class ValidarDniTest(TestCase):
    def test_dni_valido(self):
        self.assertEqual(validar_dni("12345678"), "12345678")

    def test_dni_con_letras_invalido(self):
        with self.assertRaises(ValidationError):
            validar_dni("1234567A")

    def test_dni_corto_invalido(self):
        with self.assertRaises(ValidationError):
            validar_dni("1234567")

    def test_dni_largo_invalido(self):
        with self.assertRaises(ValidationError):
            validar_dni("123456789")

    def test_dni_none_permitido(self):
        self.assertIsNone(validar_dni(None))


class ValidarTelefonoTest(TestCase):
    def test_telefono_valido(self):
        self.assertEqual(validar_telefono("987654321"), "987654321")

    def test_telefono_corto_invalido(self):
        with self.assertRaises(ValidationError):
            validar_telefono("98765432")

    def test_telefono_con_letras_invalido(self):
        with self.assertRaises(ValidationError):
            validar_telefono("98765432A")


class ValidarMontoTest(TestCase):
    def test_monto_positivo_valido(self):
        from decimal import Decimal
        self.assertEqual(validar_monto_positivo(Decimal("10.00")), Decimal("10.00"))

    def test_monto_cero_invalido(self):
        from decimal import Decimal
        with self.assertRaises(ValidationError):
            validar_monto_positivo(Decimal("0.00"))

    def test_monto_negativo_invalido(self):
        from decimal import Decimal
        with self.assertRaises(ValidationError):
            validar_monto_positivo(Decimal("-5.00"))


class ValidarCantidadTest(TestCase):
    def test_cantidad_positiva_valida(self):
        self.assertEqual(validar_cantidad_positiva(3), 3)

    def test_cantidad_cero_invalida(self):
        with self.assertRaises(ValidationError):
            validar_cantidad_positiva(0)

    def test_cantidad_negativa_invalida(self):
        with self.assertRaises(ValidationError):
            validar_cantidad_positiva(-1)
