from rest_framework import serializers
from .models import Servicio, DetalleServicio


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Servicio
        fields = ["id", "nombre_servicio", "descripcion", "precio_base", "created_at"]
        read_only_fields = ["created_at"]

    def validate_precio_base(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio base debe ser mayor a cero.")
        return value


class DetalleServicioSerializer(serializers.ModelSerializer):
    servicio_nombre = serializers.CharField(source="id_servicio.nombre_servicio", read_only=True)
    precio_base     = serializers.DecimalField(
        source="id_servicio.precio_base", max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model  = DetalleServicio
        fields = ["id", "id_prenda", "id_servicio", "servicio_nombre", "precio_base", "subtotal"]