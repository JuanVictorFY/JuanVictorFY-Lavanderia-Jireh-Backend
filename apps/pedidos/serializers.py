from rest_framework import serializers
from .models import Pedido, Prenda, EstadoPedido


class PrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Prenda
        fields = ["id", "tipo_prenda", "color", "peso", "cantidad", "observaciones"]


class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EstadoPedido
        fields = ["id", "estado", "fecha_estado", "descripcion"]


class PedidoSerializer(serializers.ModelSerializer):
    prendas         = PrendaSerializer(many=True, read_only=True)
    estados         = EstadoPedidoSerializer(many=True, read_only=True)
    cliente_nombre  = serializers.CharField(source="id_cliente.__str__", read_only=True)
    empleado_nombre = serializers.CharField(source="id_empleado.__str__", read_only=True)

    class Meta:
        model  = Pedido
        fields = [
            "id", "codigo", "cliente_nombre", "empleado_nombre",
            "fecha_ingreso", "fecha_entrega", "estado",
            "total", "observaciones", "prendas", "estados"
        ]


class CrearPedidoSerializer(serializers.Serializer):
    id_cliente    = serializers.IntegerField()
    id_empleado   = serializers.IntegerField()
    fecha_entrega = serializers.DateTimeField(required=False, allow_null=True)
    observaciones = serializers.CharField(required=False, allow_blank=True)
    prendas       = PrendaSerializer(many=True)

    def create(self, validated_data: dict) -> Pedido:
        from apps.pedidos.services import PedidoService
        prendas = validated_data.pop("prendas")
        return PedidoService.generar_pedido(prendas=prendas, **validated_data)