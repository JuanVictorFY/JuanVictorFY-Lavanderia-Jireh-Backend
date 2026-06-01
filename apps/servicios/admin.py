from django.contrib import admin
from .models import Servicio, DetalleServicio


class DetalleServicioInline(admin.TabularInline):
    model  = DetalleServicio
    extra  = 0
    fields = ["id_prenda", "subtotal"]
    readonly_fields = ["subtotal"]


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display  = ["id", "nombre_servicio", "precio_base", "descripcion"]
    search_fields = ["nombre_servicio"]
    ordering      = ["nombre_servicio"]
    inlines       = [DetalleServicioInline]


@admin.register(DetalleServicio)
class DetalleServicioAdmin(admin.ModelAdmin):
    list_display        = ["id", "id_prenda", "id_servicio", "subtotal"]
    list_select_related = ["id_prenda", "id_servicio"]
    search_fields       = ["id_servicio__nombre_servicio"]