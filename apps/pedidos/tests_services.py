from django.test import TestCase
from decimal import Decimal
from unittest.mock import patch
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado, Rol
from apps.pedidos.models import Pedido, Prenda, EstadoPedido
from apps.pedidos.services import PedidoService
from core.exceptions import RecursoNoEncontradoError, ReglaDeNegocioError
from django.contrib.auth.models import User


class PedidoServiceTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombres="Test", apellidos="Cliente", dni="33221100"
        )
        self.auth_user = User.objects.create_user(username="rec_test", password="pass")
        self.rol = Rol.objects.create(nombre_rol="recepcionista")
        self.empleado = Empleado.objects.create(
            user=self.auth_user, id_rol=self.rol,
            nombres="Test", apellidos="Empleado"
        )

    @patch("apps.pedidos.services.send_mail")
    def test_generar_pedido_con_prendas(self, mock_mail):
        prendas = [
            {"tipo_prenda": "Camisa", "color": "Blanco", "cantidad": 2, "peso": Decimal("0.5")},
            {"tipo_prenda": "Pantalon", "color": "Azul", "cantidad": 1, "peso": Decimal("1.0")},
        ]
        pedido = PedidoService.generar_pedido(
            id_cliente=self.cliente.id,
            id_empleado=self.empleado.id,
            prendas=prendas,
        )
        self.assertTrue(pedido.codigo.startswith("LAV-"))
        self.assertEqual(pedido.prendas.count(), 2)
        self.assertEqual(pedido.estado, Pedido.PENDIENTE)
        self.assertEqual(EstadoPedido.objects.filter(id_pedido=pedido).count(), 1)

    def test_generar_pedido_sin_prendas_falla(self):
        with self.assertRaises(ReglaDeNegocioError):
            PedidoService.generar_pedido(
                id_cliente=self.cliente.id,
                id_empleado=self.empleado.id,
                prendas=[],
            )

    @patch("apps.pedidos.services.send_mail")
    def test_cambiar_estado_exitoso(self, mock_mail):
        pedido = Pedido.objects.create(
            id_cliente=self.cliente,
            id_empleado=self.empleado,
        )
        PedidoService.cambiar_estado(pedido.id, Pedido.EN_PROCESO, "Ingresado a maquina")
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, Pedido.EN_PROCESO)

    @patch("apps.pedidos.services.send_mail")
    def test_cambiar_estado_invalido_falla(self, mock_mail):
        pedido = Pedido.objects.create(
            id_cliente=self.cliente,
            id_empleado=self.empleado,
        )
        with self.assertRaises(ReglaDeNegocioError):
            PedidoService.cambiar_estado(pedido.id, "estado_invalido")

    def test_obtener_pedido_por_codigo(self):
        pedido = Pedido.objects.create(
            id_cliente=self.cliente,
            id_empleado=self.empleado,
        )
        resultado = PedidoService.obtener_pedido_por_codigo(pedido.codigo)
        self.assertEqual(resultado["codigo"], pedido.codigo)
        self.assertIn("historial", resultado)

    def test_pedido_no_encontrado_por_codigo(self):
        with self.assertRaises(RecursoNoEncontradoError):
            PedidoService.obtener_pedido_por_codigo("NOEXISTE")
