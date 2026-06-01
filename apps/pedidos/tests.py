from django.test import TestCase
from .models import Pedido, Prenda, EstadoPedido
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado, Rol
from django.contrib.auth.models import User


class PedidoModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombres="Ana", apellidos="Torres", dni="44445555"
        )
        self.user = User.objects.create_user(username="emp1", password="pass123")
        self.rol = Rol.objects.create(nombre_rol="Recepcionista")
        self.empleado = Empleado.objects.create(
            user=self.user, id_rol=self.rol,
            nombres="Carlos", apellidos="Ruiz"
        )
        self.pedido = Pedido.objects.create(
            id_cliente=self.empleado and self.cliente,
            id_empleado=self.empleado,
        )

    def test_codigo_generado_automaticamente(self):
        self.assertTrue(self.pedido.codigo.startswith("LAV-"))
        self.assertEqual(len(self.pedido.codigo), 10)

    def test_estado_inicial_pendiente(self):
        self.assertEqual(self.pedido.estado, Pedido.PENDIENTE)

    def test_str_representation(self):
        self.assertIn("LAV-", str(self.pedido))


class PrendaModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombres="Rosa", apellidos="Mamani", dni="55556666"
        )
        self.user = User.objects.create_user(username="emp2", password="pass123")
        self.rol = Rol.objects.create(nombre_rol="Operario")
        self.empleado = Empleado.objects.create(
            user=self.user, id_rol=self.rol,
            nombres="Pedro", apellidos="Vargas"
        )
        self.pedido = Pedido.objects.create(
            id_cliente=self.cliente,
            id_empleado=self.empleado,
        )

    def test_crear_prenda(self):
        prenda = Prenda.objects.create(
            id_pedido=self.pedido,
            tipo_prenda="Camisa",
            color="Blanco",
            cantidad=3,
        )
        self.assertEqual(str(prenda), "Camisa — Pedido #1")
        self.assertEqual(self.pedido.prendas.count(), 1)
