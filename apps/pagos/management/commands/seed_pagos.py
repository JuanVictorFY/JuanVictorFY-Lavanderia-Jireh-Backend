from django.core.management.base import BaseCommand
from decimal import Decimal
import random
from apps.pedidos.models import Pedido
from apps.pagos.models import Pago


METODOS = [Pago.EFECTIVO, Pago.YAPE, Pago.PLIN, Pago.TRANSFERENCIA, Pago.TARJETA]


class Command(BaseCommand):
    help = "Carga pagos de ejemplo asociados a pedidos existentes"

    def handle(self, *args, **options):
        pedidos_sin_pago = Pedido.objects.exclude(pagos__isnull=False).filter(
            estado__in=[Pedido.LISTO, Pedido.ENTREGADO]
        )
        if not pedidos_sin_pago.exists():
            self.stdout.write(self.style.WARNING("No hay pedidos listos sin pago. Genera pedidos primero."))
            return

        creados = 0
        for pedido in pedidos_sin_pago:
            monto = pedido.total if pedido.total > 0 else Decimal(str(round(random.uniform(15.0, 80.0), 2)))
            Pago.objects.create(
                id_pedido=pedido,
                monto=monto,
                metodo_pago=random.choice(METODOS),
                estado_pago=Pago.PAGADO,
            )
            creados += 1

        self.stdout.write(self.style.SUCCESS(f"{creados} pagos demo creados."))
