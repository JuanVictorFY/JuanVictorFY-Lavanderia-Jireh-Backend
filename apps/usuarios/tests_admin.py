from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from .models import Rol, Empleado
from .admin import RolAdmin, EmpleadoAdmin


class RolAdminTest(TestCase):
    def setUp(self):
        self.site  = AdminSite()
        self.admin = RolAdmin(Rol, self.site)

    def test_search_fields_configurado(self):
        self.assertIn("nombre_rol", self.admin.search_fields)

    def test_ordering_configurado(self):
        self.assertIn("nombre_rol", self.admin.ordering)


class EmpleadoAdminTest(TestCase):
    def setUp(self):
        self.site  = AdminSite()
        self.admin = EmpleadoAdmin(Empleado, self.site)

    def test_list_display_tiene_rol(self):
        self.assertIn("id_rol", self.admin.list_display)

    def test_list_filter_tiene_estado(self):
        self.assertIn("estado", self.admin.list_filter)

    def test_list_editable_tiene_estado(self):
        self.assertIn("estado", self.admin.list_editable)

    def test_fieldsets_configurados(self):
        self.assertIsNotNone(self.admin.fieldsets)
        self.assertGreater(len(self.admin.fieldsets), 1)
