from django.test import TestCase, RequestFactory
from unittest.mock import MagicMock, patch
from .middleware import AuditoriaEmpleadoMiddleware


class AuditoriaMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.get_response = MagicMock(return_value=MagicMock(status_code=200))
        self.middleware = AuditoriaEmpleadoMiddleware(self.get_response)

    def test_middleware_llama_get_response(self):
        request = self.factory.get("/api/test/")
        request.user = MagicMock(is_authenticated=False)
        response = self.middleware(request)
        self.get_response.assert_called_once_with(request)

    def test_middleware_con_usuario_no_autenticado(self):
        request = self.factory.get("/api/test/")
        request.user = MagicMock(is_authenticated=False)
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_middleware_con_empleado_autenticado(self):
        request = self.factory.get("/api/empleados/")
        empleado = MagicMock()
        empleado.id_rol.nombre_rol = "recepcionista"
        request.user = MagicMock(is_authenticated=True, empleado=empleado)
        with patch("apps.usuarios.middleware.logger") as mock_logger:
            response = self.middleware(request)
            mock_logger.debug.assert_called_once()
