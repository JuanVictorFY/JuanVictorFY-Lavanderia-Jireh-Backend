from django.contrib import admin
from .models import CacheReporte


@admin.register(CacheReporte)
class CacheReporteAdmin(admin.ModelAdmin):
    list_display    = ["id", "tipo", "fecha_ref", "generado_en"]
    list_filter     = ["tipo"]
    readonly_fields = ["generado_en", "datos_json"]
    ordering        = ["-fecha_ref"]
    search_fields   = ["fecha_ref"]
