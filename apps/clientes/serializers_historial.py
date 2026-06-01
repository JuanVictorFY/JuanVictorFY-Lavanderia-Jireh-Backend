from rest_framework import serializers
from .models import Cliente
from apps.pedidos.models import Pedido


class PedidoResumenSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model  = Pedido
        fields = ["id", "codigo", "estado", "estado_display", "total", "fecha_ingreso", "fecha_entrega"]


class ClienteHistorialSerializer(serializers.ModelSerializer):
    pedidos          = PedidoResumenSerializer(many=True, read_only=True)
    total_pedidos    = serializers.SerializerMethodField()
    gasto_acumulado  = serializers.SerializerMethodField()

    class Meta:
        model  = Cliente
        fields = [
            "id", "nombres", "apellidos", "dni", "correo", "telefono",
            "fecha_registro", "total_pedidos", "gasto_acumulado", "pedidos",
        ]

    def get_total_pedidos(self, obj):
        return obj.pedidos.count()

    def get_gasto_acumulado(self, obj):
        from django.db.models import Sum
        total = obj.pedidos.aggregate(t=Sum("total"))["t"]
        return float(total or 0)
