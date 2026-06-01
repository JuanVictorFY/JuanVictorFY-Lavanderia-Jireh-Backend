from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from .models import CacheReporte
from .admin import CacheReporteAdmin


class CacheReporteAdminTest(TestCase):
    def setUp(self):
        self.site  = AdminSite()
        self.admin = CacheReporteAdmin(CacheReporte, self.site)

    def test_list_display_tiene_tipo(self):
        self.assertIn("tipo", self.admin.list_display)

    def test_list_display_tiene_fecha(self):
        self.assertIn("fecha_ref", self.admin.list_display)

    def test_list_filter_tiene_tipo(self):
        self.assertIn("tipo", self.admin.list_filter)

    def test_readonly_generado_en(self):
        self.assertIn("generado_en", self.admin.readonly_fields)

    def test_str_cache_reporte(self):
        from datetime import date
        reporte = CacheReporte(
            tipo=CacheReporte.TIPO_DIARIO,
            fecha_ref=date.today(),
            datos_json={}
        )
        self.assertIn("diario", str(reporte).lower())
