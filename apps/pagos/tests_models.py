from django.test import TestCase
from .models import Pago
from apps.pedidos.models import Pedido
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado, Rol
from django.contrib.auth.models import User
from decimal import Decimal


class PagoModelMetaTest(TestCase):
    def test_db_table(self):
        self.assertEqual(Pago._meta.db_table, "pago")

    def test_ordering_por_fecha(self):
        self.assertIn("-fecha_pago", Pago._meta.ordering)

    def test_estados_disponibles(self):
        estados = [e[0] for e in Pago.ESTADOS_PAGO]
        self.assertIn(Pago.PENDIENTE, estados)
        self.assertIn(Pago.PAGADO, estados)
        self.assertIn(Pago.ANULADO, estados)

    def test_metodos_disponibles(self):
        metodos = [m[0] for m in Pago.METODOS]
        self.assertIn(Pago.EFECTIVO, metodos)
        self.assertIn(Pago.YAPE, metodos)
        self.assertIn(Pago.PLIN, metodos)
        self.assertIn(Pago.TRANSFERENCIA, metodos)
        self.assertIn(Pago.TARJETA, metodos)

    def test_monto_tiene_2_decimales(self):
        field = Pago._meta.get_field("monto")
        self.assertEqual(field.decimal_places, 2)
