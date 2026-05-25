from django.contrib import admin
from .models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display  = ["id", "id_pedido", "monto", "metodo_pago", "estado_pago", "fecha_pago"]
    list_filter   = ["metodo_pago", "estado_pago"]
    search_fields = ["id_pedido__id"]