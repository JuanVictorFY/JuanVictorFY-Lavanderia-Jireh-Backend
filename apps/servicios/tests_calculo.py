from django.test import TestCase
from decimal import Decimal
from unittest.mock import patch, MagicMock
from .services import ServicioService
from .models import Servicio, DetalleServicio
from apps.pedidos.models import Prenda, Pedido
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado, Rol
from django.contrib.auth.models import User


class CalculoSubtotalTest(TestCase):
    def setUp(self):
        self.servicio = Servicio.objects.create(
            nombre_servicio="Lavado Test",
            precio_base=Decimal("10.00"),
        )
        self.cliente = Cliente.objects.create(nombres="Test", apellidos="Cliente", dni="11112222")
        self.user = Rol.objects.create(nombre_rol="operario")
        self.auth_user = User.objects.create_user(username="op_test", password="pass123")
        self.empleado = Empleado.objects.create(
            user=self.auth_user, id_rol=self.user,
            nombres="Test", apellidos="Empleado"
        )
        self.pedido = Pedido.objects.create(
            id_cliente=self.cliente,
            id_empleado=self.empleado,
        )
        self.prenda = Prenda.objects.create(
            id_pedido=self.pedido,
            tipo_prenda="Camisa",
            peso=Decimal("1.50"),
            cantidad=2,
        )

    def test_subtotal_incluye_cantidad(self):
        detalle = ServicioService.calcular_subtotal(self.prenda.id, self.servicio.id)
        esperado = Decimal("10.00") * Decimal("1.50") * Decimal("2")
        self.assertEqual(detalle.subtotal, esperado)

    def test_subtotal_con_peso_cero(self):
        self.prenda.peso = Decimal("0.00")
        self.prenda.save()
        detalle = ServicioService.calcular_subtotal(self.prenda.id, self.servicio.id)
        self.assertEqual(detalle.subtotal, Decimal("0.00"))

    def test_subtotal_cantidad_uno(self):
        self.prenda.cantidad = 1
        self.prenda.peso = Decimal("2.00")
        self.prenda.save()
        detalle = ServicioService.calcular_subtotal(self.prenda.id, self.servicio.id)
        self.assertEqual(detalle.subtotal, Decimal("20.00"))

    def test_prenda_no_encontrada_lanza_error(self):
        from core.exceptions import RecursoNoEncontradoError
        with self.assertRaises(RecursoNoEncontradoError):
            ServicioService.calcular_subtotal(99999, self.servicio.id)

    def test_servicio_no_encontrado_lanza_error(self):
        from core.exceptions import RecursoNoEncontradoError
        with self.assertRaises(RecursoNoEncontradoError):
            ServicioService.calcular_subtotal(self.prenda.id, 99999)
