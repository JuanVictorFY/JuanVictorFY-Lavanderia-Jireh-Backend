from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random
from apps.clientes.models import Cliente
from apps.usuarios.models import Empleado
from apps.pedidos.models import Pedido, Prenda


TIPOS_PRENDA = ["Camisa", "Pantalon", "Vestido", "Casaca", "Polo", "Chompa", "Edredon", "Sabana", "Toalla"]
COLORES      = ["Blanco", "Negro", "Azul", "Rojo", "Verde", "Gris", "Beige", None]
ESTADOS      = [Pedido.PENDIENTE, Pedido.EN_PROCESO, Pedido.LISTO, Pedido.ENTREGADO]


class Command(BaseCommand):
    help = "Carga pedidos de ejemplo en la base de datos"

    def add_arguments(self, parser):
        parser.add_argument("--cantidad", type=int, default=20)

    def handle(self, *args, **options):
        clientes  = list(Cliente.objects.all())
        empleados = list(Empleado.objects.filter(estado=True))

        if not clientes or not empleados:
            self.stdout.write(self.style.ERROR("Se necesitan clientes y empleados. Ejecuta seed_clientes y seed_roles primero."))
            return

        creados = 0
        cantidad = options["cantidad"]

        for i in range(cantidad):
            cliente  = random.choice(clientes)
            empleado = random.choice(empleados)
            estado   = random.choice(ESTADOS)
            dias_atras = random.randint(0, 30)

            pedido = Pedido(
                id_cliente=cliente,
                id_empleado=empleado,
                estado=estado,
                total=Decimal("0.00"),
                observaciones=f"Pedido demo #{i + 1}",
            )
            pedido.save()

            num_prendas = random.randint(1, 5)
            for _ in range(num_prendas):
                Prenda.objects.create(
                    id_pedido=pedido,
                    tipo_prenda=random.choice(TIPOS_PRENDA),
                    color=random.choice(COLORES),
                    cantidad=random.randint(1, 4),
                    peso=round(random.uniform(0.3, 3.0), 2),
                )
            creados += 1

        self.stdout.write(self.style.SUCCESS(f"{creados} pedidos demo creados exitosamente."))
