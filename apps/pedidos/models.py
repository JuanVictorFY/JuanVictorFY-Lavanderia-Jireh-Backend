import uuid
from django.db import models
from core.models import TimeStampedModel


class Pedido(TimeStampedModel):
    PENDIENTE  = "pendiente"
    EN_PROCESO = "en_proceso"
    LISTO      = "listo"
    ENTREGADO  = "entregado"
    CANCELADO  = "cancelado"

    ESTADOS = [
        (PENDIENTE,  "Pendiente"),
        (EN_PROCESO, "En Proceso"),
        (LISTO,      "Listo para entrega"),
        (ENTREGADO,  "Entregado"),
        (CANCELADO,  "Cancelado"),
    ]

    codigo      = models.CharField(max_length=10, unique=True, editable=False)
    id_cliente  = models.ForeignKey(
        "clientes.Cliente", on_delete=models.RESTRICT,
        db_column="id_cliente", related_name="pedidos"
    )
    id_empleado = models.ForeignKey(
        "usuarios.Empleado", on_delete=models.RESTRICT,
        db_column="id_empleado", related_name="pedidos"
    )
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    estado        = models.CharField(max_length=30, choices=ESTADOS, default=PENDIENTE)
    total         = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "pedido"
        ordering = ["-fecha_ingreso"]

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self._generar_codigo()
        super().save(*args, **kwargs)

    @staticmethod
    def _generar_codigo():
        return "LAV-" + uuid.uuid4().hex[:6].upper()

    def __str__(self):
        return f"Pedido #{self.id} [{self.codigo}] — {self.id_cliente}"


class Prenda(TimeStampedModel):
    id_pedido     = models.ForeignKey(
        Pedido, on_delete=models.CASCADE,
        db_column="id_pedido", related_name="prendas"
    )
    tipo_prenda   = models.CharField(max_length=100)
    color         = models.CharField(max_length=50, blank=True, null=True)
    peso          = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    cantidad      = models.IntegerField(default=1)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "prenda"

    def __str__(self):
        return f"{self.tipo_prenda} — Pedido #{self.id_pedido_id}"


class EstadoPedido(TimeStampedModel):
    id_pedido    = models.ForeignKey(
        Pedido, on_delete=models.CASCADE,
        db_column="id_pedido", related_name="estados"
    )
    estado       = models.CharField(max_length=30)
    fecha_estado = models.DateTimeField(auto_now_add=True)
    descripcion  = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "estado_pedido"
        ordering = ["-fecha_estado"]

    def __str__(self):
        return f"Pedido #{self.id_pedido_id} → {self.estado}"