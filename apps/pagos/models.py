from django.db import models
from core.models import TimeStampedModel


class Pago(TimeStampedModel):
    EFECTIVO      = "efectivo"
    TARJETA       = "tarjeta"
    TRANSFERENCIA = "transferencia"
    YAPE          = "yape"
    PLIN          = "plin"

    METODOS = [
        (EFECTIVO,      "Efectivo"),
        (TARJETA,       "Tarjeta"),
        (TRANSFERENCIA, "Transferencia"),
        (YAPE,          "Yape"),
        (PLIN,          "Plin"),
    ]

    PENDIENTE = "pendiente"
    PAGADO    = "pagado"
    ANULADO   = "anulado"

    ESTADOS_PAGO = [
        (PENDIENTE, "Pendiente"),
        (PAGADO,    "Pagado"),
        (ANULADO,   "Anulado"),
    ]

    id_pedido   = models.ForeignKey(
        "pedidos.Pedido", on_delete=models.RESTRICT,
        db_column="id_pedido", related_name="pagos"
    )
    monto       = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=30, choices=METODOS, default=EFECTIVO)
    fecha_pago  = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default=PENDIENTE)

    class Meta:
        db_table = "pago"
        ordering = ["-fecha_pago"]

    def __str__(self):
        return f"Pago #{self.id} — S/{self.monto} — {self.estado_pago}"