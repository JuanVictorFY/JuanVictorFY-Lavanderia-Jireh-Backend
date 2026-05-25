import logging
from decimal import Decimal
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from core.exceptions import ReglaDeNegocioError, RecursoNoEncontradoError
from .models import Pedido, Prenda, EstadoPedido


logger = logging.getLogger("lavanderia")


MENSAJES_ESTADO = {
    Pedido.EN_PROCESO: (
        "Tu pedido está en proceso",
        "Tus prendas ya ingresaron a lavado. Estaremos listos pronto."
    ),
    Pedido.LISTO: (
        "Tu pedido está listo para recoger",
        "Tus prendas ya están listas. Puedes pasar a recogerlas."
    ),
    Pedido.ENTREGADO: (
        "Pedido entregado — ¡Gracias!",
        "Hemos entregado tu pedido exitosamente. ¡Gracias por confiar en Lavanderia Jireh!"
    ),
}


class PedidoService:

    @staticmethod
    @transaction.atomic
    def generar_pedido(id_cliente: int, id_empleado: int, prendas: list,
                       fecha_entrega=None, observaciones: str = "") -> Pedido:
        if not prendas:
            raise ReglaDeNegocioError("El pedido debe tener al menos una prenda.")

        pedido = Pedido.objects.create(
            id_cliente_id=id_cliente,
            id_empleado_id=id_empleado,
            estado=Pedido.PENDIENTE,
            fecha_entrega=fecha_entrega,
            observaciones=observaciones,
            total=Decimal("0.00"),
        )
        for datos in prendas:
            Prenda.objects.create(id_pedido=pedido, **datos)

        EstadoPedido.objects.create(
            id_pedido=pedido,
            estado=Pedido.PENDIENTE,
            descripcion="Pedido registrado en el sistema.",
        )
        return pedido

    @staticmethod
    def calcular_total(pedido: Pedido) -> Decimal:
        from apps.servicios.models import DetalleServicio
        detalles = DetalleServicio.objects.filter(id_prenda__id_pedido=pedido)
        total = sum((d.subtotal for d in detalles), Decimal("0.00"))
        pedido.total = total
        pedido.save(update_fields=["total", "updated_at"])
        return total

    @staticmethod
    def obtener_pedido_por_id(id_pedido: int) -> Pedido:
        try:
            return Pedido.objects.get(pk=id_pedido)
        except Pedido.DoesNotExist:
            raise RecursoNoEncontradoError(f"Pedido {id_pedido} no encontrado.")

    @staticmethod
    def obtener_pedido_por_codigo(codigo: str) -> dict:
        try:
            pedido = Pedido.objects.select_related("id_cliente").prefetch_related("estados").get(codigo=codigo)
        except Pedido.DoesNotExist:
            raise RecursoNoEncontradoError(f"Código '{codigo}' no encontrado.")

        return {
            "codigo":        pedido.codigo,
            "cliente":       f"{pedido.id_cliente.nombres} {pedido.id_cliente.apellidos}",
            "estado_actual": pedido.estado,
            "fecha_ingreso": pedido.fecha_ingreso,
            "fecha_entrega": pedido.fecha_entrega,
            "total":         str(pedido.total),
            "historial": [
                {
                    "estado":      e.estado,
                    "descripcion": e.descripcion,
                    "fecha":       e.fecha_estado,
                }
                for e in pedido.estados.order_by("fecha_estado")
            ]
        }

    @staticmethod
    @transaction.atomic
    def cambiar_estado(id_pedido: int, nuevo_estado: str, descripcion: str = "") -> EstadoPedido:
        try:
            pedido = Pedido.objects.select_related("id_cliente").get(pk=id_pedido)
        except Pedido.DoesNotExist:
            raise RecursoNoEncontradoError(f"Pedido {id_pedido} no encontrado.")

        estados_validos = [e[0] for e in Pedido.ESTADOS]
        if nuevo_estado not in estados_validos:
            raise ReglaDeNegocioError(f"Estado '{nuevo_estado}' no válido.")

        pedido.estado = nuevo_estado
        pedido.save(update_fields=["estado", "updated_at"])

        estado_obj = EstadoPedido.objects.create(
            id_pedido=pedido,
            estado=nuevo_estado,
            descripcion=descripcion,
        )

        PedidoService._enviar_correo_estado(pedido, nuevo_estado)

        return estado_obj

    @staticmethod
    def _enviar_correo_estado(pedido: Pedido, nuevo_estado: str) -> None:
        cliente = pedido.id_cliente
        if not cliente.correo or nuevo_estado not in MENSAJES_ESTADO:
            return

        asunto, cuerpo = MENSAJES_ESTADO[nuevo_estado]
        url_consulta   = f"{settings.FRONTEND_URL}/pedido/{pedido.codigo}/"

        mensaje = (
            f"Hola {cliente.nombres},\n\n"
            f"{cuerpo}\n\n"
            f"──────────────────────────────\n"
            f"Código de tu pedido : {pedido.codigo}\n"
            f"Estado actual       : {nuevo_estado.replace('_', ' ').title()}\n"
            f"Consulta tu pedido  : {url_consulta}\n"
            f"──────────────────────────────\n\n"
            f"— Lavanderia Jireh\n"
        )

        try:
            send_mail(
                subject=f"{asunto} — Código: {pedido.codigo}",
                message=mensaje,
                from_email=None,
                recipient_list=[cliente.correo],
                fail_silently=False,
            )
            logger.info("Correo enviado a %s — pedido %s", cliente.correo, pedido.codigo)
        except Exception as exc:
            logger.error("Error enviando correo a %s: %s", cliente.correo, str(exc))