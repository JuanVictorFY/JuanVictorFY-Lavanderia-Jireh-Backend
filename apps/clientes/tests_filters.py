from django.test import TestCase
from apps.clientes.filters import ClienteFilter
from apps.clientes.models import Cliente


class ClienteFilterTest(TestCase):
    def setUp(self):
        Cliente.objects.create(nombres="Maria", apellidos="Quispe", dni="12345678", correo="maria@test.com")
        Cliente.objects.create(nombres="Juan", apellidos="Mamani", dni="87654321", correo="juan@test.com")
        Cliente.objects.create(nombres="Rosa", apellidos="Condori", dni="11223344")

    def test_filtrar_por_nombre(self):
        f = ClienteFilter(data={"nombres": "maria"}, queryset=Cliente.objects.all())
        self.assertEqual(f.qs.count(), 1)

    def test_filtrar_por_apellido(self):
        f = ClienteFilter(data={"apellidos": "mam"}, queryset=Cliente.objects.all())
        self.assertEqual(f.qs.count(), 1)

    def test_filtrar_por_dni(self):
        f = ClienteFilter(data={"dni": "1234"}, queryset=Cliente.objects.all())
        self.assertEqual(f.qs.count(), 1)

    def test_filtrar_sin_resultados(self):
        f = ClienteFilter(data={"nombres": "noexiste"}, queryset=Cliente.objects.all())
        self.assertEqual(f.qs.count(), 0)

    def test_sin_filtros_devuelve_todos(self):
        f = ClienteFilter(data={}, queryset=Cliente.objects.all())
        self.assertEqual(f.qs.count(), 3)
