from django.test import TestCase
from decimal import Decimal
from apps.servicios.filters import ServicioFilter
from apps.servicios.models import Servicio


class ServicioFilterTest(TestCase):
    def setUp(self):
        Servicio.objects.create(nombre_servicio="Lavado Normal", precio_base=Decimal("12.00"))
        Servicio.objects.create(nombre_servicio="Lavado Delicado", precio_base=Decimal("25.00"))
        Servicio.objects.create(nombre_servicio="Planchado", precio_base=Decimal("8.00"))

    def test_filtrar_por_nombre_parcial(self):
        f = ServicioFilter(data={"nombre_servicio": "lavado"}, queryset=Servicio.objects.all())
        self.assertEqual(f.qs.count(), 2)

    def test_filtrar_por_precio_min(self):
        f = ServicioFilter(data={"precio_min": "15"}, queryset=Servicio.objects.all())
        self.assertEqual(f.qs.count(), 1)

    def test_filtrar_por_precio_max(self):
        f = ServicioFilter(data={"precio_max": "10"}, queryset=Servicio.objects.all())
        self.assertEqual(f.qs.count(), 1)

    def test_sin_filtros_todos(self):
        f = ServicioFilter(data={}, queryset=Servicio.objects.all())
        self.assertEqual(f.qs.count(), 3)
