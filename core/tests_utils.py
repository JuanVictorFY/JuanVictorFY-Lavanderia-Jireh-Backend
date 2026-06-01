from django.test import TestCase
from decimal import Decimal
from datetime import datetime
from core.utils import (
    formatear_fecha_peru, generar_codigo_recibo, calcular_igv
)


class FormatearFechaPeruTest(TestCase):
    def test_fecha_formateada_correctamente(self):
        dt = datetime(2026, 6, 1, 14, 30)
        self.assertEqual(formatear_fecha_peru(dt), "01/06/2026 14:30")

    def test_fecha_none_retorna_vacio(self):
        self.assertEqual(formatear_fecha_peru(None), "")


class GenerarCodigoReciboTest(TestCase):
    def test_formato_correcto(self):
        codigo = generar_codigo_recibo(1)
        self.assertTrue(codigo.startswith("REC-"))
        self.assertIn("-0001", codigo)

    def test_codigo_con_id_grande(self):
        codigo = generar_codigo_recibo(9999)
        self.assertIn("-9999", codigo)

    def test_codigos_distintos_por_id(self):
        c1 = generar_codigo_recibo(1)
        c2 = generar_codigo_recibo(2)
        self.assertNotEqual(c1, c2)


class CalcularIgvTest(TestCase):
    def test_igv_18_por_ciento(self):
        resultado = calcular_igv(Decimal("100.00"))
        self.assertEqual(resultado, Decimal("18.00"))

    def test_igv_personalizado(self):
        resultado = calcular_igv(Decimal("100.00"), porcentaje=10.0)
        self.assertEqual(resultado, Decimal("10.00"))

    def test_igv_redondeo(self):
        resultado = calcular_igv(Decimal("33.33"))
        self.assertEqual(resultado, Decimal("6.00"))
