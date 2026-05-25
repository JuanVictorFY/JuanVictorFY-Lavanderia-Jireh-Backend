from rest_framework import serializers
from .models import Pago


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Pago
        fields = ["id", "id_pedido", "monto", "metodo_pago", "fecha_pago", "estado_pago"]