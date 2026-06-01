from django.test import TestCase
from decimal import Decimal
from .models import Servicio
from .serializers import ServicioSerializer


class ServicioSerializerTest(TestCase):
    def test_campos_requeridos(self):
        data = {"nombre_servicio": "Lavado X", "precio_base": "18.00"}
        s = ServicioSerializer(data=data)
        self.assertTrue(s.is_valid(), s.errors)

    def test_precio_cero_invalido(self):
        data = {"nombre_servicio": "Prueba", "precio_base": "0.00"}
        s = ServicioSerializer(data=data)
        self.assertFalse(s.is_valid())
        self.assertIn("precio_base", s.errors)

    def test_precio_negativo_invalido(self):
        data = {"nombre_servicio": "Prueba", "precio_base": "-5.00"}
        s = ServicioSerializer(data=data)
        self.assertFalse(s.is_valid())

    def test_serializar_servicio_existente(self):
        servicio = Servicio.objects.create(nombre_servicio="Dry Clean", precio_base=Decimal("40.00"))
        data = ServicioSerializer(servicio).data
        self.assertEqual(data["nombre_servicio"], "Dry Clean")
        self.assertIn("created_at", data)
