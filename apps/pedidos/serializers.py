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
    prendas            = PrendaSerializer(many=True, read_only=True)
    estados            = EstadoPedidoSerializer(many=True, read_only=True)
    cliente_id         = serializers.IntegerField(source="id_cliente.id", read_only=True)
    cliente_nombre     = serializers.CharField(source="id_cliente.__str__", read_only=True)
    cliente_dni        = serializers.CharField(source="id_cliente.dni", read_only=True, default=None)
    cliente_telefono   = serializers.CharField(source="id_cliente.telefono", read_only=True, default=None)
    cliente_correo     = serializers.EmailField(source="id_cliente.correo", read_only=True, default=None)
    cliente_direccion  = serializers.CharField(source="id_cliente.direccion", read_only=True, default=None)
    empleado_nombre    = serializers.CharField(source="id_empleado.__str__", read_only=True)

    class Meta:
        model  = Pedido
        fields = [
            "id", "codigo",
            "cliente_id", "cliente_nombre", "cliente_dni",
            "cliente_telefono", "cliente_correo", "cliente_direccion",
            "empleado_nombre",
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