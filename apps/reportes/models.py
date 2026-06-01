from django.db import models
from core.models import TimeStampedModel


class CacheReporte(TimeStampedModel):
    TIPO_DIARIO   = "diario"
    TIPO_MENSUAL  = "mensual"
    TIPO_ANUAL    = "anual"

    TIPOS = [
        (TIPO_DIARIO,  "Diario"),
        (TIPO_MENSUAL, "Mensual"),
        (TIPO_ANUAL,   "Anual"),
    ]

    tipo        = models.CharField(max_length=20, choices=TIPOS)
    fecha_ref   = models.DateField()
    datos_json  = models.JSONField()
    generado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table        = "cache_reporte"
        unique_together = [("tipo", "fecha_ref")]
        ordering        = ["-fecha_ref"]

    def __str__(self):
        return f"Reporte {self.tipo} — {self.fecha_ref}"
