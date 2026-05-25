from django.db import models
from core.models import TimeStampedModel


class Servicio(TimeStampedModel):
    nombre_servicio = models.CharField(max_length=100, unique=True)
    descripcion     = models.TextField(blank=True, null=True)
    precio_base     = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "servicio"
        ordering = ["nombre_servicio"]

    def __str__(self):
        return self.nombre_servicio


class DetalleServicio(TimeStampedModel):
    id_prenda   = models.ForeignKey(
        "pedidos.Prenda", on_delete=models.CASCADE,
        db_column="id_prenda", related_name="detalles"
    )
    id_servicio = models.ForeignKey(
        Servicio, on_delete=models.RESTRICT,
        db_column="id_servicio", related_name="detalles"
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = "detalle_servicio"

    def __str__(self):
        return f"Detalle #{self.id} — {self.id_servicio}"