from django.test import TestCase
from decimal import Decimal
from apps.pagos.filters import PagoFilter
from apps.pagos.models import Pago
from apps.pedidos.models import Pedido
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado, Rol
from django.contrib.auth.models import User


class PagoFilterTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nombres="Test", apellidos="Pago", dni="55550000")
        self.user = User.objects.create_user(username="cajero_f", password="pass")
        self.rol = Rol.objects.create(nombre_rol="cajero_f")
        self.empleado = Empleado.objects.create(
            user=self.user, id_rol=self.rol, nombres="Test", apellidos="Cajero"
        )
        self.pedido = Pedido.objects.create(
            id_cliente=self.cliente, id_empleado=self.empleado
        )
        Pago.objects.create(id_pedido=self.pedido, monto=Decimal("30.00"), metodo_pago=Pago.YAPE, estado_pago=Pago.PAGADO)
        Pago.objects.create(id_pedido=self.pedido, monto=Decimal("60.00"), metodo_pago=Pago.EFECTIVO, estado_pago=Pago.PENDIENTE)

    def test_filtrar_por_metodo(self):
        f = PagoFilter(data={"metodo_pago": "yape"}, queryset=Pago.objects.all())
        self.assertEqual(f.qs.count(), 1)

    def test_filtrar_por_estado(self):
        f = PagoFilter(data={"estado_pago": "pagado"}, queryset=Pago.objects.all())
        self.assertEqual(f.qs.count(), 1)

    def test_filtrar_por_monto_min(self):
        f = PagoFilter(data={"monto_min": "50"}, queryset=Pago.objects.all())
        self.assertEqual(f.qs.count(), 1)

    def test_filtrar_sin_filtros(self):
        f = PagoFilter(data={}, queryset=Pago.objects.all())
        self.assertEqual(f.qs.count(), 2)
