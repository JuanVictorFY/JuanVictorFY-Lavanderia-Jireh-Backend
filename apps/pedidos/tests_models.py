from django.test import TestCase
from .models import Pedido, Prenda, EstadoPedido
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado, Rol
from django.contrib.auth.models import User
from decimal import Decimal


class PedidoModelMetaTest(TestCase):
    def test_db_table(self):
        self.assertEqual(Pedido._meta.db_table, "pedido")

    def test_ordering_por_fecha(self):
        self.assertIn("-fecha_ingreso", Pedido._meta.ordering)

    def test_estados_constants(self):
        self.assertEqual(Pedido.PENDIENTE, "pendiente")
        self.assertEqual(Pedido.EN_PROCESO, "en_proceso")
        self.assertEqual(Pedido.LISTO, "listo")
        self.assertEqual(Pedido.ENTREGADO, "entregado")
        self.assertEqual(Pedido.CANCELADO, "cancelado")

    def test_codigo_prefijo_lav(self):
        codigo = Pedido._generar_codigo()
        self.assertTrue(codigo.startswith("LAV-"))
        self.assertEqual(len(codigo), 10)

    def test_codigos_son_unicos(self):
        codigos = {Pedido._generar_codigo() for _ in range(50)}
        self.assertEqual(len(codigos), 50)


class PrendaModelMetaTest(TestCase):
    def test_db_table(self):
        self.assertEqual(Prenda._meta.db_table, "prenda")

    def test_cantidad_default(self):
        field = Prenda._meta.get_field("cantidad")
        self.assertEqual(field.default, 1)
