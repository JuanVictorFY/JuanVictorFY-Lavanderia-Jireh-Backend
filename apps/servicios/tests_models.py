from django.test import TestCase
from decimal import Decimal
from .models import Servicio, DetalleServicio
from apps.pedidos.models import Pedido, Prenda
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado, Rol
from django.contrib.auth.models import User


class ServicioModelTest(TestCase):
    def test_nombre_max_length(self):
        field = Servicio._meta.get_field("nombre_servicio")
        self.assertEqual(field.max_length, 100)

    def test_nombre_unico(self):
        field = Servicio._meta.get_field("nombre_servicio")
        self.assertTrue(field.unique)

    def test_precio_base_decimales(self):
        field = Servicio._meta.get_field("precio_base")
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(field.max_digits, 10)

    def test_db_table(self):
        self.assertEqual(Servicio._meta.db_table, "servicio")

    def test_ordering(self):
        self.assertIn("nombre_servicio", Servicio._meta.ordering)


class DetalleServicioModelTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nombres="Det", apellidos="Test", dni="66665555")
        self.user = User.objects.create_user(username="det_user", password="pass")
        self.rol = Rol.objects.create(nombre_rol="det_rol")
        self.empleado = Empleado.objects.create(
            user=self.user, id_rol=self.rol, nombres="Det", apellidos="Emp"
        )
        self.pedido = Pedido.objects.create(id_cliente=self.cliente, id_empleado=self.empleado)
        self.servicio = Servicio.objects.create(nombre_servicio="Det Srv", precio_base=Decimal("10.00"))
        self.prenda = Prenda.objects.create(id_pedido=self.pedido, tipo_prenda="Camisa", cantidad=1)

    def test_crear_detalle(self):
        detalle = DetalleServicio.objects.create(
            id_prenda=self.prenda,
            id_servicio=self.servicio,
            subtotal=Decimal("10.00"),
        )
        self.assertIn("Detalle", str(detalle))
        self.assertEqual(detalle.subtotal, Decimal("10.00"))
