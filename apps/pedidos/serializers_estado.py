from rest_framework import serializers
from .models import Pedido, EstadoPedido


class CambiarEstadoPedidoSerializer(serializers.Serializer):
    nuevo_estado = serializers.ChoiceField(choices=Pedido.ESTADOS)
    descripcion  = serializers.CharField(max_length=500, required=False, allow_blank=True)


class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EstadoPedido
        fields = ["id", "estado", "descripcion", "fecha_estado"]
        read_only_fields = ["fecha_estado"]
