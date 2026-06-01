from django.test import TestCase
from datetime import date
from apps.reportes.utils import (
    rango_semana_actual, rango_mes_actual,
    rango_anio_actual, porcentaje_cambio
)


class RangoFechasTest(TestCase):
    def test_semana_actual_inicio_es_lunes(self):
        inicio, fin = rango_semana_actual()
        self.assertEqual(inicio.weekday(), 0)

    def test_semana_actual_fin_es_hoy(self):
        _, fin = rango_semana_actual()
        self.assertEqual(fin, date.today())

    def test_mes_actual_inicio_es_dia_1(self):
        inicio, _ = rango_mes_actual()
        self.assertEqual(inicio.day, 1)

    def test_anio_actual_inicio_es_enero_1(self):
        inicio, _ = rango_anio_actual()
        self.assertEqual(inicio.month, 1)
        self.assertEqual(inicio.day, 1)


class PorcentajeCambioTest(TestCase):
    def test_aumento_100_por_ciento(self):
        self.assertEqual(porcentaje_cambio(100, 50), 100.0)

    def test_disminucion(self):
        self.assertEqual(porcentaje_cambio(50, 100), -50.0)

    def test_sin_cambio(self):
        self.assertEqual(porcentaje_cambio(100, 100), 0.0)

    def test_desde_cero_con_valor(self):
        self.assertEqual(porcentaje_cambio(50, 0), 100.0)

    def test_ambos_cero(self):
        self.assertEqual(porcentaje_cambio(0, 0), 0.0)
