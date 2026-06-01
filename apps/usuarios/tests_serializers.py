from django.test import TestCase
from django.contrib.auth.models import User
from .models import Rol, Empleado
from .serializers import RolSerializer, EmpleadoSerializer, CambiarContrasenaSerializer


class RolSerializerTest(TestCase):
    def test_serializar_rol(self):
        rol = Rol.objects.create(nombre_rol="test_rol")
        data = RolSerializer(rol).data
        self.assertEqual(data["nombre_rol"], "test_rol")
        self.assertIn("id", data)


class CambiarContrasenaSerializerTest(TestCase):
    def test_contrasenas_coinciden(self):
        data = {
            "nueva_contrasena":    "Nueva1234!",
            "confirmar_contrasena": "Nueva1234!",
        }
        s = CambiarContrasenaSerializer(data=data)
        self.assertTrue(s.is_valid())

    def test_contrasenas_no_coinciden(self):
        data = {
            "nueva_contrasena":    "Nueva1234!",
            "confirmar_contrasena": "Diferente99!",
        }
        s = CambiarContrasenaSerializer(data=data)
        self.assertFalse(s.is_valid())

    def test_contrasena_requerida(self):
        s = CambiarContrasenaSerializer(data={})
        self.assertFalse(s.is_valid())
