from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Empleado, Rol
from .services import EmpleadoService
from core.exceptions import RecursoNoEncontradoError, ReglaDeNegocioError


class EmpleadoServiceTest(TestCase):
    def setUp(self):
        self.rol_admin = Rol.objects.create(nombre_rol="administrador")
        self.rol_operario = Rol.objects.create(nombre_rol="operario")
        self.user = User.objects.create_user(username="emp_roles", password="pass123")
        self.empleado = Empleado.objects.create(
            user=self.user, id_rol=self.rol_operario,
            nombres="Test", apellidos="Empleado", estado=True
        )

    def test_cambiar_rol(self):
        actualizado = EmpleadoService.cambiar_rol(self.empleado.id, self.rol_admin.id)
        self.assertEqual(actualizado.id_rol, self.rol_admin)

    def test_cambiar_rol_inexistente_falla(self):
        with self.assertRaises((RecursoNoEncontradoError, Exception)):
            EmpleadoService.cambiar_rol(self.empleado.id, 99999)

    def test_actualizar_estado_activo(self):
        actualizado = EmpleadoService.actualizar_estado(self.empleado.id, False)
        self.assertFalse(actualizado.estado)

    def test_actualizar_estado_inactivo(self):
        self.empleado.estado = False
        self.empleado.save()
        actualizado = EmpleadoService.actualizar_estado(self.empleado.id, True)
        self.assertTrue(actualizado.estado)

    def test_empleado_no_encontrado(self):
        with self.assertRaises(RecursoNoEncontradoError):
            EmpleadoService.actualizar_estado(99999, True)
