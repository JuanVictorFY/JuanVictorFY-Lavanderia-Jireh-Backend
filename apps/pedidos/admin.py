from django.contrib import admin
from .models import Pedido, Prenda, EstadoPedido


class PrendaInline(admin.TabularInline):
    model  = Prenda
    extra  = 0
    fields = ["tipo_prenda", "color", "peso", "cantidad", "observaciones"]


class EstadoPedidoInline(admin.TabularInline):
    model     = EstadoPedido
    extra     = 0
    fields    = ["estado", "descripcion", "fecha_estado"]
    readonly_fields = ["fecha_estado"]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display        = ["id", "codigo", "id_cliente", "id_empleado", "estado", "total", "fecha_ingreso"]
    list_filter         = ["estado", "fecha_ingreso"]
    search_fields       = ["codigo", "id_cliente__nombres", "id_cliente__apellidos"]
    readonly_fields     = ["codigo", "fecha_ingreso"]
    list_select_related = ["id_cliente", "id_empleado"]
    inlines             = [PrendaInline, EstadoPedidoInline]


@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display  = ["id", "tipo_prenda", "color", "peso", "cantidad", "id_pedido"]
    search_fields = ["tipo_prenda", "color"]
    list_filter   = ["tipo_prenda"]


@admin.register(EstadoPedido)
class EstadoPedidoAdmin(admin.ModelAdmin):
    list_display    = ["id", "id_pedido", "estado", "fecha_estado"]
    list_filter     = ["estado"]
    readonly_fields = ["fecha_estado"]