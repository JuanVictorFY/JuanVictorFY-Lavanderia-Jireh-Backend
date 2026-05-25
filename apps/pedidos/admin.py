from django.contrib import admin
from .models import Pedido, Prenda, EstadoPedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display  = ["id", "id_cliente", "id_empleado", "estado", "total", "fecha_ingreso"]
    list_filter   = ["estado"]
    search_fields = ["id_cliente__nombres", "id_cliente__apellidos"]


@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display  = ["id", "tipo_prenda", "color", "peso", "cantidad", "id_pedido"]
    search_fields = ["tipo_prenda"]


@admin.register(EstadoPedido)
class EstadoPedidoAdmin(admin.ModelAdmin):
    list_display = ["id", "id_pedido", "estado", "fecha_estado"]
    list_filter  = ["estado"]