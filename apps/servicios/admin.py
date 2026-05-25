from django.contrib import admin
from .models import Servicio, DetalleServicio


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display  = ["id", "nombre_servicio", "precio_base"]
    search_fields = ["nombre_servicio"]


@admin.register(DetalleServicio)
class DetalleServicioAdmin(admin.ModelAdmin):
    list_display = ["id", "id_prenda", "id_servicio", "subtotal"]