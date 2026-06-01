from django.test import TestCase
from decimal import Decimal
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado, Rol
from apps.pedidos.models import Pedido
from apps.pagos.models import Pago
from apps.pagos.services import PagoService
from core.exceptions import RecursoNoEncontradoError, ReglaDeNegocioError
from django.contrib.auth.models import User


class PagoServiceTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nombres="Test", apellidos="Cliente", dni="11223300")
        self.auth_user = User.objects.create_user(username="cajero", password="pass")
        self.rol = Rol.objects.create(nombre_rol="cajero")
        self.empleado = Empleado.objects.create(
            user=self.auth_user, id_rol=self.rol,
            nombres="Test", apellidos="Cajero"
        )
        self.pedido = Pedido.objects.create(
            id_cliente=self.cliente,
            id_empleado=self.empleado,
            total=Decimal("50.00"),
        )

    def test_registrar_pago_exitoso(self):
        pago = PagoService.registrar_pago(self.pedido.id, Decimal("50.00"), Pago.YAPE)
        self.assertEqual(pago.estado_pago, Pago.PENDIENTE)
        self.assertEqual(pago.monto, Decimal("50.00"))

    def test_registrar_pago_pedido_cancelado_falla(self):
        self.pedido.estado = Pedido.CANCELADO
        self.pedido.save()
        with self.assertRaises(ReglaDeNegocioError):
            PagoService.registrar_pago(self.pedido.id, Decimal("50.00"), Pago.EFECTIVO)

    def test_registrar_pago_monto_cero_falla(self):
        with self.assertRaises(ReglaDeNegocioError):
            PagoService.registrar_pago(self.pedido.id, Decimal("0.00"), Pago.EFECTIVO)

    def test_confirmar_pago(self):
        pago = PagoService.registrar_pago(self.pedido.id, Decimal("30.00"), Pago.EFECTIVO)
        confirmado = PagoService.confirmar_pago(pago.id)
        self.assertEqual(confirmado.estado_pago, Pago.PAGADO)

    def test_confirmar_pago_ya_pagado_falla(self):
        pago = PagoService.registrar_pago(self.pedido.id, Decimal("30.00"), Pago.EFECTIVO)
        PagoService.confirmar_pago(pago.id)
        with self.assertRaises(ReglaDeNegocioError):
            PagoService.confirmar_pago(pago.id)

    def test_anular_pago(self):
        pago = PagoService.registrar_pago(self.pedido.id, Decimal("20.00"), Pago.TRANSFERENCIA)
        anulado = PagoService.anular_pago(pago.id)
        self.assertEqual(anulado.estado_pago, Pago.ANULADO)

    def test_pago_inexistente_falla(self):
        with self.assertRaises(RecursoNoEncontradoError):
            PagoService.confirmar_pago(99999)
