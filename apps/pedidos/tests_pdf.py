from django.test import TestCase
from unittest.mock import MagicMock, patch
from io import BytesIO
from .pdf_utils import generar_buffer_recibo


class GenerarBufferReciboTest(TestCase):
    def _mock_pedido(self):
        prenda = MagicMock()
        prenda.tipo_prenda = "Camisa"
        prenda.color = "Blanco"
        prenda.cantidad = 2
        prenda.peso = 0.5

        pedido = MagicMock()
        pedido.codigo = "LAV-ABCD12"
        pedido.total = 30.00
        pedido.get_estado_display.return_value = "Pendiente"
        pedido.fecha_ingreso.strftime.return_value = "01/06/2026 10:00"
        pedido.prendas.all.return_value = [prenda]
        return pedido

    def test_retorna_bytes_io(self):
        pedido = self._mock_pedido()
        buffer = generar_buffer_recibo(pedido)
        self.assertIsInstance(buffer, BytesIO)

    def test_buffer_no_vacio(self):
        pedido = self._mock_pedido()
        buffer = generar_buffer_recibo(pedido)
        contenido = buffer.read()
        self.assertGreater(len(contenido), 100)

    def test_buffer_es_pdf(self):
        pedido = self._mock_pedido()
        buffer = generar_buffer_recibo(pedido)
        inicio = buffer.read(5)
        self.assertEqual(inicio, b"%PDF-")
