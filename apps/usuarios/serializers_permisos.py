from rest_framework import serializers
from .models import Rol, Empleado


class RolResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Rol
        fields = ["id", "nombre_rol"]


class EmpleadoPerfilSerializer(serializers.ModelSerializer):
    rol     = RolResumenSerializer(source="id_rol", read_only=True)
    usuario = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model  = Empleado
        fields = ["id", "nombres", "apellidos", "telefono", "estado", "rol", "usuario"]


class CambiarRolSerializer(serializers.Serializer):
    id_rol = serializers.IntegerField()

    def validate_id_rol(self, value):
        if not Rol.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"El rol con id={value} no existe.")
        return value


class CambiarEstadoSerializer(serializers.Serializer):
    estado = serializers.BooleanField()
