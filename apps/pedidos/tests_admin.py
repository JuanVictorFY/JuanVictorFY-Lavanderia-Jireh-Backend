from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from .models import Pedido, Prenda, EstadoPedido
from .admin import PedidoAdmin, PrendaAdmin, EstadoPedidoAdmin


class PedidoAdminTest(TestCase):
    def setUp(self):
        self.site  = AdminSite()
        self.admin = PedidoAdmin(Pedido, self.site)

    def test_list_display_tiene_codigo(self):
        self.assertIn("codigo", self.admin.list_display)

    def test_readonly_fields_tiene_codigo(self):
        self.assertIn("codigo", self.admin.readonly_fields)

    def test_inlines_configurados(self):
        self.assertTrue(len(self.admin.inlines) >= 2)

    def test_list_filter_por_estado(self):
        self.assertIn("estado", self.admin.list_filter)


class PrendaAdminTest(TestCase):
    def setUp(self):
        self.site  = AdminSite()
        self.admin = PrendaAdmin(Prenda, self.site)

    def test_search_fields_configurado(self):
        self.assertTrue(len(self.admin.search_fields) > 0)

    def test_list_display_tiene_tipo_prenda(self):
        self.assertIn("tipo_prenda", self.admin.list_display)
