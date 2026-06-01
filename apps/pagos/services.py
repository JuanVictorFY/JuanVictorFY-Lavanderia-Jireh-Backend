from decimal import Decimal
from django.db import transaction
from core.exceptions import ReglaDeNegocioError, RecursoNoEncontradoError
from .models import Pago


class PagoService:

    @staticmethod
    @transaction.atomic
    def registrar_pago(id_pedido: int, monto: Decimal, metodo_pago: str) -> Pago:
        from apps.pedidos.models import Pedido
        try:
            pedido = Pedido.objects.get(pk=id_pedido)
        except Pedido.DoesNotExist:
            raise RecursoNoEncontradoError(f"Pedido {id_pedido} no encontrado.")

        if pedido.estado == Pedido.CANCELADO:
            raise ReglaDeNegocioError("No se puede pagar un pedido cancelado.")

        if monto <= 0:
            raise ReglaDeNegocioError("El monto del pago debe ser mayor a cero.")

        return Pago.objects.create(
            id_pedido=pedido,
            monto=monto,
            metodo_pago=metodo_pago,
            estado_pago=Pago.PENDIENTE,
        )

    @staticmethod
    def confirmar_pago(id_pago: int) -> Pago:
        try:
            pago = Pago.objects.get(pk=id_pago)
        except Pago.DoesNotExist:
            raise RecursoNoEncontradoError(f"Pago {id_pago} no encontrado.")

        if pago.estado_pago != Pago.PENDIENTE:
            raise ReglaDeNegocioError("Solo se pueden confirmar pagos pendientes.")

        pago.estado_pago = Pago.PAGADO
        pago.save(update_fields=["estado_pago", "updated_at"])
        return pago

    @staticmethod
    def anular_pago(id_pago: int) -> Pago:
        try:
            pago = Pago.objects.get(pk=id_pago)
        except Pago.DoesNotExist:
            raise RecursoNoEncontradoError(f"Pago {id_pago} no encontrado.")

        if pago.estado_pago == Pago.ANULADO:
            raise ReglaDeNegocioError("El pago ya está anulado.")

        pago.estado_pago = Pago.ANULADO
        pago.save(update_fields=["estado_pago", "updated_at"])
        return pago