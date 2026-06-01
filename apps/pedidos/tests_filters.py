from django.test import TestCase
from apps.pedidos.filters import PedidoFilter
from apps.pedidos.models import Pedido


class PedidoFilterTest(TestCase):
    def test_filter_campos_definidos(self):
        campos = PedidoFilter.Meta.fields
        self.assertIn("estado", campos)
        self.assertIn("codigo", campos)

    def test_filter_estado_choices_validos(self):
        estados_validos = [e[0] for e in Pedido.ESTADOS]
        self.assertIn("pendiente",  estados_validos)
        self.assertIn("entregado",  estados_validos)
        self.assertIn("cancelado",  estados_validos)
