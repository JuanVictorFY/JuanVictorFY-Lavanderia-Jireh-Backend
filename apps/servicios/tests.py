from django.test import TestCase
from .models import Servicio, DetalleServicio
from decimal import Decimal


class ServicioModelTest(TestCase):
    def setUp(self):
        self.servicio = Servicio.objects.create(
            nombre_servicio="Lavado Normal",
            descripcion="Lavado y secado estandar",
            precio_base=Decimal("15.00"),
        )

    def test_str_representation(self):
        self.assertEqual(str(self.servicio), "Lavado Normal")

    def test_precio_base_correcto(self):
        self.assertEqual(self.servicio.precio_base, Decimal("15.00"))

    def test_nombre_unico(self):
        with self.assertRaises(Exception):
            Servicio.objects.create(
                nombre_servicio="Lavado Normal",
                precio_base=Decimal("20.00"),
            )

    def test_crear_multiples_servicios(self):
        Servicio.objects.create(nombre_servicio="Planchado", precio_base=Decimal("10.00"))
        Servicio.objects.create(nombre_servicio="Lavado Delicado", precio_base=Decimal("25.00"))
        self.assertEqual(Servicio.objects.count(), 3)
