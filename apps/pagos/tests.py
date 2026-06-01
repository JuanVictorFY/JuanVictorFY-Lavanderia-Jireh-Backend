from django.test import TestCase
from .models import Pago
from apps.pedidos.models import Pedido
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado, Rol
from django.contrib.auth.models import User
from decimal import Decimal


class PagoModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombres="Luis", apellidos="Condori", dni="77778888"
        )
        self.user = User.objects.create_user(username="cajero1", password="pass123")
        self.rol = Rol.objects.create(nombre_rol="Cajero")
        self.empleado = Empleado.objects.create(
            user=self.user, id_rol=self.rol,
            nombres="Elena", apellidos="Huanca"
        )
        self.pedido = Pedido.objects.create(
            id_cliente=self.cliente,
            id_empleado=self.empleado,
            total=Decimal("50.00"),
        )

    def test_crear_pago(self):
        pago = Pago.objects.create(
            id_pedido=self.pedido,
            monto=Decimal("50.00"),
            metodo_pago=Pago.YAPE,
        )
        self.assertEqual(pago.estado_pago, Pago.PENDIENTE)
        self.assertEqual(pago.monto, Decimal("50.00"))

    def test_str_representation(self):
        pago = Pago.objects.create(
            id_pedido=self.pedido,
            monto=Decimal("25.00"),
            metodo_pago=Pago.EFECTIVO,
        )
        self.assertIn("S/25.00", str(pago))

    def test_metodos_pago_disponibles(self):
        metodos = [m[0] for m in Pago.METODOS]
        self.assertIn("yape", metodos)
        self.assertIn("efectivo", metodos)
        self.assertIn("transferencia", metodos)
