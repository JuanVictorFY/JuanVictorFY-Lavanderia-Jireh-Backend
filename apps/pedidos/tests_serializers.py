from django.test import TestCase
from .serializers_estado import CambiarEstadoPedidoSerializer
from .models import Pedido


class CambiarEstadoPedidoSerializerTest(TestCase):
    def test_estado_valido(self):
        s = CambiarEstadoPedidoSerializer(data={"nuevo_estado": Pedido.EN_PROCESO})
        self.assertTrue(s.is_valid(), s.errors)

    def test_estado_invalido(self):
        s = CambiarEstadoPedidoSerializer(data={"nuevo_estado": "estado_falso"})
        self.assertFalse(s.is_valid())

    def test_descripcion_opcional(self):
        s = CambiarEstadoPedidoSerializer(data={"nuevo_estado": Pedido.LISTO})
        self.assertTrue(s.is_valid())

    def test_descripcion_con_texto(self):
        s = CambiarEstadoPedidoSerializer(data={
            "nuevo_estado": Pedido.ENTREGADO,
            "descripcion": "Entregado al cliente",
        })
        self.assertTrue(s.is_valid())
        self.assertEqual(s.validated_data["descripcion"], "Entregado al cliente")
