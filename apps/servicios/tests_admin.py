from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from decimal import Decimal
from .models import Servicio, DetalleServicio
from .admin import ServicioAdmin, DetalleServicioAdmin


class ServicioAdminTest(TestCase):
    def setUp(self):
        self.site  = AdminSite()
        self.admin = ServicioAdmin(Servicio, self.site)
        self.servicio = Servicio.objects.create(
            nombre_servicio="Planchado Test",
            precio_base=Decimal("12.00"),
        )

    def test_list_display_contiene_campos(self):
        self.assertIn("nombre_servicio", self.admin.list_display)
        self.assertIn("precio_base", self.admin.list_display)

    def test_search_fields_configurado(self):
        self.assertIn("nombre_servicio", self.admin.search_fields)

    def test_str_servicio(self):
        self.assertEqual(str(self.servicio), "Planchado Test")
