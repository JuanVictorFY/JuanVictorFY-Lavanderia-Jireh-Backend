from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from .models import Cliente, PersonaAutorizada
from .admin import ClienteAdmin, PersonaAutorizadaAdmin


class ClienteAdminTest(TestCase):
    def setUp(self):
        self.site  = AdminSite()
        self.admin = ClienteAdmin(Cliente, self.site)

    def test_list_display_contiene_dni(self):
        self.assertIn("dni", self.admin.list_display)

    def test_search_fields_incluye_dni(self):
        self.assertIn("dni", self.admin.search_fields)

    def test_readonly_fecha_registro(self):
        self.assertIn("fecha_registro", self.admin.readonly_fields)

    def test_inlines_configurados(self):
        self.assertTrue(len(self.admin.inlines) > 0)


class PersonaAutorizadaAdminTest(TestCase):
    def setUp(self):
        self.site  = AdminSite()
        self.admin = PersonaAutorizadaAdmin(PersonaAutorizada, self.site)

    def test_list_display_contiene_dni(self):
        self.assertIn("dni", self.admin.list_display)

    def test_search_fields_por_dni(self):
        self.assertIn("dni", self.admin.search_fields)
