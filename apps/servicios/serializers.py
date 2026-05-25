from rest_framework import serializers
from .models import Servicio, DetalleServicio


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Servicio
        fields = ["id", "nombre_servicio", "descripcion", "precio_base"]


class DetalleServicioSerializer(serializers.ModelSerializer):
    servicio_nombre = serializers.CharField(source="id_servicio.nombre_servicio", read_only=True)

    class Meta:
        model  = DetalleServicio
        fields = ["id", "id_prenda", "id_servicio", "servicio_nombre", "subtotal"]