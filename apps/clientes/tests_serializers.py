from django.test import TestCase
from .models import Cliente
from .serializers import RegistroClienteSerializer, ClienteSerializer


class RegistroClienteSerializerTest(TestCase):
    def test_registro_valido(self):
        data = {
            "nombres": "Test",
            "apellidos": "Usuario",
            "dni": "12345678",
            "correo": "test@email.com",
        }
        s = RegistroClienteSerializer(data=data)
        self.assertTrue(s.is_valid(), s.errors)

    def test_correo_duplicado_invalido(self):
        Cliente.objects.create(
            nombres="Existente", apellidos="Cliente",
            correo="duplicado@email.com"
        )
        data = {"nombres": "Nuevo", "apellidos": "Cliente", "correo": "duplicado@email.com"}
        s = RegistroClienteSerializer(data=data)
        self.assertFalse(s.is_valid())
        self.assertIn("correo", s.errors)

    def test_campos_opcionales_no_requeridos(self):
        data = {"nombres": "Solo", "apellidos": "Nombre"}
        s = RegistroClienteSerializer(data=data)
        self.assertTrue(s.is_valid(), s.errors)
