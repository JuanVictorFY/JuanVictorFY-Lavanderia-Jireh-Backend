from django.test import TestCase
from unittest.mock import MagicMock
from rest_framework.response import Response
from core.exceptions import (
    ReglaDeNegocioError, RecursoNoEncontradoError,
    PermisoDenegadoError, DatosInvalidosError,
    custom_exception_handler,
)


def make_context():
    view = MagicMock()
    view.__class__.__name__ = "TestView"
    return {"view": view, "request": MagicMock()}


class ExceptionHandlerTest(TestCase):
    def test_regla_negocio_retorna_400(self):
        resp = custom_exception_handler(
            ReglaDeNegocioError("No permitido"), make_context()
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.data)

    def test_recurso_no_encontrado_retorna_404(self):
        resp = custom_exception_handler(
            RecursoNoEncontradoError("No existe"), make_context()
        )
        self.assertEqual(resp.status_code, 404)

    def test_permiso_denegado_retorna_403(self):
        resp = custom_exception_handler(
            PermisoDenegadoError("Sin permiso"), make_context()
        )
        self.assertEqual(resp.status_code, 403)

    def test_datos_invalidos_retorna_422(self):
        resp = custom_exception_handler(
            DatosInvalidosError("Datos incorrectos"), make_context()
        )
        self.assertEqual(resp.status_code, 422)

    def test_error_inesperado_retorna_500(self):
        resp = custom_exception_handler(
            RuntimeError("Boom"), make_context()
        )
        self.assertEqual(resp.status_code, 500)
        self.assertIn("error", resp.data)
