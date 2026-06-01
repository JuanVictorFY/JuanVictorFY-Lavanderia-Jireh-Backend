from django.test import TestCase
from datetime import date, timedelta
from decimal import Decimal
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado, Rol
from apps.pedidos.models import Pedido
from apps.pagos.models import Pago
from apps.reportes.services import ReporteService
from django.contrib.auth.models import User


class ReporteServiceTest(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nombres="Ana", apellidos="Lopez", dni="11111111")
        self.user = User.objects.create_user(username="rpt_user", password="pass")
        self.rol = Rol.objects.create(nombre_rol="administrador")
        self.empleado = Empleado.objects.create(
            user=self.user, id_rol=self.rol, nombres="Admin", apellidos="Test"
        )
        self.pedido = Pedido.objects.create(
            id_cliente=self.cliente, id_empleado=self.empleado, total=Decimal("40.00")
        )
        Pago.objects.create(
            id_pedido=self.pedido,
            monto=Decimal("40.00"),
            metodo_pago=Pago.YAPE,
            estado_pago=Pago.PAGADO,
        )

    def test_resumen_por_rango_retorna_dict(self):
        hoy = date.today()
        resultado = ReporteService.resumen_por_rango(hoy - timedelta(days=1), hoy)
        self.assertIn("total_pedidos", resultado)
        self.assertIn("ingresos_totales", resultado)
        self.assertGreaterEqual(resultado["total_pedidos"], 1)

    def test_clientes_frecuentes(self):
        resultado = ReporteService.clientes_frecuentes(limite=5)
        self.assertIsInstance(resultado, list)
        self.assertGreaterEqual(len(resultado), 1)

    def test_ingresos_por_dia(self):
        resultado = ReporteService.ingresos_por_dia(dias=7)
        self.assertEqual(len(resultado), 7)
        self.assertIn("fecha", resultado[0])
        self.assertIn("total", resultado[0])

    def test_resumen_rango_sin_datos(self):
        hace_un_anio = date.today() - timedelta(days=365)
        resultado = ReporteService.resumen_por_rango(hace_un_anio, hace_un_anio)
        self.assertEqual(resultado["total_pedidos"], 0)
        self.assertEqual(resultado["ingresos_totales"], 0.0)
