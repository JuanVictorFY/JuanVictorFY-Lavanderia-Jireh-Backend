from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Cliente, PersonaAutorizada


class ClienteModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombres="Juan",
            apellidos="Perez",
            dni="12345678",
            telefono="999888777",
            correo="juan@test.com",
        )

    def test_str_representation(self):
        self.assertEqual(str(self.cliente), "Juan Perez")

    def test_cliente_created_successfully(self):
        self.assertEqual(Cliente.objects.count(), 1)

    def test_correo_unique(self):
        with self.assertRaises(Exception):
            Cliente.objects.create(
                nombres="Pedro",
                apellidos="Lopez",
                correo="juan@test.com",
            )


class PersonaAutorizadaModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombres="Maria",
            apellidos="Garcia",
            dni="87654321",
        )
        self.persona = PersonaAutorizada.objects.create(
            id_cliente=self.cliente,
            nombres="Luis Garcia",
            dni="11223344",
            telefono="911000111",
        )

    def test_str_representation(self):
        self.assertIn("Luis Garcia", str(self.persona))

    def test_persona_relacionada_con_cliente(self):
        self.assertEqual(self.cliente.personas_autorizadas.count(), 1)
