from rest_framework import serializers
from .models import Pago


class ComprobanteSerializer(serializers.ModelSerializer):
    pedido_codigo  = serializers.CharField(source="id_pedido.codigo", read_only=True)
    cliente        = serializers.SerializerMethodField()
    metodo_display = serializers.CharField(source="get_metodo_pago_display", read_only=True)
    estado_display = serializers.CharField(source="get_estado_pago_display", read_only=True)

    class Meta:
        model  = Pago
        fields = [
            "id", "pedido_codigo", "cliente", "monto",
            "metodo_pago", "metodo_display", "estado_pago", "estado_display",
            "fecha_pago",
        ]

    def get_cliente(self, obj):
        c = obj.id_pedido.id_cliente
        return {"nombre": str(c), "dni": c.dni, "telefono": c.telefono}
