from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from apps.usuarios.models import Empleado, Rol


class AnalyticsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="admin_test", password="pass1234")
        self.rol = Rol.objects.create(nombre_rol="administrador")
        self.empleado = Empleado.objects.create(
            user=self.user, id_rol=self.rol,
            nombres="Admin", apellidos="Test", estado=True
        )
        self.client.force_authenticate(user=self.user)

    def test_analytics_returns_200(self):
        url = reverse("reportes:analytics")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_analytics_contiene_resumen(self):
        url = reverse("reportes:analytics")
        response = self.client.get(url)
        data = response.json()
        self.assertIn("resumen", data)
        self.assertIn("pedidos_hoy", data["resumen"])
        self.assertIn("ingresos_hoy", data["resumen"])

    def test_analytics_contiene_estados(self):
        url = reverse("reportes:analytics")
        response = self.client.get(url)
        data = response.json()
        self.assertIn("pedidos_por_estado", data)

    def test_no_autenticado_recibe_401(self):
        self.client.logout()
        url = reverse("reportes:analytics")
        response = self.client.get(url)
        self.assertIn(response.status_code, [401, 403])
