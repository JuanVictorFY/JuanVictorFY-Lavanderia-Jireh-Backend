from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from .models import Pago
from .admin import PagoAdmin


class PagoAdminTest(TestCase):
    def setUp(self):
        self.site  = AdminSite()
        self.admin = PagoAdmin(Pago, self.site)

    def test_list_display_tiene_monto(self):
        self.assertIn("monto", self.admin.list_display)

    def test_list_display_tiene_metodo_pago(self):
        self.assertIn("metodo_pago", self.admin.list_display)

    def test_list_filter_tiene_estado(self):
        self.assertIn("estado_pago", self.admin.list_filter)

    def test_readonly_fecha_pago(self):
        self.assertIn("fecha_pago", self.admin.readonly_fields)

    def test_ordering_por_fecha(self):
        self.assertEqual(self.admin.ordering, ["-fecha_pago"])
