from django.test import TestCase
from core.mixins import SoftDeleteMixin, OrdenamientoMixin, BusquedaMixin


class SoftDeleteMixinTest(TestCase):
    def test_mixin_existe(self):
        self.assertTrue(hasattr(SoftDeleteMixin, "destroy"))

    def test_ordenamiento_mixin_defaults(self):
        self.assertEqual(OrdenamientoMixin.ordering, ["-created_at"])
        self.assertIn("created_at", OrdenamientoMixin.ordering_fields)

    def test_busqueda_mixin_search_fields_vacio(self):
        self.assertEqual(BusquedaMixin.search_fields, [])
