from django.test import TestCase
from django.contrib.auth.models import User
from .models import Empleado, Rol
from core.permissions import (
    EsAdministrador, EsEmpleadoActivo,
    EsAdministradorORecepcionista, EsRecepcionista, EsOperario,
)
from unittest.mock import Mock


def make_request(nombre_rol, activo=True):
    user = Mock()
    user.is_authenticated = True
    user.empleado.id_rol.nombre_rol = nombre_rol
    user.empleado.estado = activo
    return user


class EsAdministradorTest(TestCase):
    def test_admin_tiene_permiso(self):
        perm = EsAdministrador()
        req = Mock(user=make_request("administrador"))
        self.assertTrue(perm.has_permission(req, None))

    def test_recepcionista_no_tiene_permiso(self):
        perm = EsAdministrador()
        req = Mock(user=make_request("recepcionista"))
        self.assertFalse(perm.has_permission(req, None))


class EsEmpleadoActivoTest(TestCase):
    def test_empleado_activo_pasa(self):
        perm = EsEmpleadoActivo()
        req = Mock(user=make_request("operario", activo=True))
        self.assertTrue(perm.has_permission(req, None))

    def test_empleado_inactivo_bloqueado(self):
        perm = EsEmpleadoActivo()
        req = Mock(user=make_request("operario", activo=False))
        self.assertFalse(perm.has_permission(req, None))


class EsAdministradorORecepcionistaTest(TestCase):
    def test_admin_pasa(self):
        perm = EsAdministradorORecepcionista()
        req = Mock(user=make_request("administrador"))
        self.assertTrue(perm.has_permission(req, None))

    def test_recepcionista_pasa(self):
        perm = EsAdministradorORecepcionista()
        req = Mock(user=make_request("recepcionista"))
        self.assertTrue(perm.has_permission(req, None))

    def test_operario_bloqueado(self):
        perm = EsAdministradorORecepcionista()
        req = Mock(user=make_request("operario"))
        self.assertFalse(perm.has_permission(req, None))
