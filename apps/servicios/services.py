from decimal import Decimal
from core.exceptions import RecursoNoEncontradoError
from .models import Servicio, DetalleServicio


class ServicioService:

    @staticmethod
    def calcular_subtotal(id_prenda: int, id_servicio: int) -> DetalleServicio:
        from apps.pedidos.models import Prenda
        try:
            prenda   = Prenda.objects.get(pk=id_prenda)
            servicio = Servicio.objects.get(pk=id_servicio)
        except Prenda.DoesNotExist:
            raise RecursoNoEncontradoError(f"Prenda {id_prenda} no encontrada.")
        except Servicio.DoesNotExist:
            raise RecursoNoEncontradoError(f"Servicio {id_servicio} no encontrado.")

        # subtotal = precio_base * peso de la prenda
        subtotal = Decimal(str(servicio.precio_base)) * Decimal(str(prenda.peso))

        detalle, _ = DetalleServicio.objects.update_or_create(
            id_prenda=prenda,
            id_servicio=servicio,
            defaults={"subtotal": subtotal},
        )
        return detalle