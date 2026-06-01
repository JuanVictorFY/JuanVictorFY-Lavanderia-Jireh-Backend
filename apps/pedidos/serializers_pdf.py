from rest_framework import serializers
from .models import Pedido, Prenda


class PrendaReciboSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Prenda
        fields = ["tipo_prenda", "color", "cantidad", "peso", "observaciones"]


class PedidoReciboSerializer(serializers.ModelSerializer):
    cliente  = serializers.SerializerMethodField()
    empleado = serializers.SerializerMethodField()
    prendas  = PrendaReciboSerializer(many=True, read_only=True)
    estado   = serializers.CharField(source="get_estado_display")

    class Meta:
        model  = Pedido
        fields = [
            "id", "codigo", "cliente", "empleado",
            "fecha_ingreso", "fecha_entrega", "estado",
            "total", "observaciones", "prendas",
        ]

    def get_cliente(self, obj):
        c = obj.id_cliente
        return {"id": c.id, "nombre": str(c), "telefono": c.telefono}

    def get_empleado(self, obj):
        e = obj.id_empleado
        return {"id": e.id, "nombre": str(e)}
