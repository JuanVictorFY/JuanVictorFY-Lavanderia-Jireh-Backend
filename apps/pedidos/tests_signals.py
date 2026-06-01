from django.test import TestCase
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado, Rol
from apps.pedidos.models import Pedido, EstadoPedido
from django.contrib.auth.models import User


class PedidoSignalTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nombres="Signal", apellidos="Test", dni="99998888")
        self.user = User.objects.create_user(username="sig_user", password="pass")
        self.rol = Rol.objects.create(nombre_rol="recepcionista_sig")
        self.empleado = Empleado.objects.create(
            user=self.user, id_rol=self.rol, nombres="Sig", apellidos="Emp"
        )

    def test_estado_inicial_creado_automaticamente(self):
        pedido = Pedido.objects.create(
            id_cliente=self.cliente,
            id_empleado=self.empleado,
        )
        estados = EstadoPedido.objects.filter(id_pedido=pedido)
        self.assertEqual(estados.count(), 1)
        self.assertEqual(estados.first().estado, Pedido.PENDIENTE)

    def test_descripcion_estado_inicial(self):
        pedido = Pedido.objects.create(
            id_cliente=self.cliente,
            id_empleado=self.empleado,
        )
        estado = EstadoPedido.objects.filter(id_pedido=pedido).first()
        self.assertIn("sistema", estado.descripcion.lower())
