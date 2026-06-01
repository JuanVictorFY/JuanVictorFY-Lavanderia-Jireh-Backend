from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Rol, Empleado


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Rol
        fields = ["id", "nombre_rol"]


class EmpleadoSerializer(serializers.ModelSerializer):
    rol_nombre = serializers.CharField(source="id_rol.nombre_rol", read_only=True)
    usuario    = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model  = Empleado
        fields = ["id", "nombres", "apellidos", "telefono", "estado", "rol_nombre", "usuario"]


class CrearEmpleadoSerializer(serializers.Serializer):
    usuario    = serializers.CharField(max_length=150)
    contrasena = serializers.CharField(write_only=True, min_length=8)
    nombres    = serializers.CharField(max_length=100)
    apellidos  = serializers.CharField(max_length=100)
    telefono   = serializers.CharField(max_length=20, required=False, allow_blank=True)
    id_rol     = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all())

    def validate_usuario(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("El nombre de usuario ya está en uso.")
        return value

    def create(self, validated_data: dict) -> Empleado:
        from apps.usuarios.services import EmpleadoService
        return EmpleadoService.crear_empleado(**validated_data)


class ActualizarEmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Empleado
        fields = ["nombres", "apellidos", "telefono", "id_rol"]


class CambiarContrasenaSerializer(serializers.Serializer):
    nueva_contrasena = serializers.CharField(write_only=True, min_length=8)


# JWT con datos del empleado en el payload
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if hasattr(user, "empleado"):
            token["nombres"]       = user.empleado.nombres
            token["apellidos"]     = user.empleado.apellidos
            token["rol"]           = user.empleado.id_rol.nombre_rol
            token["estado"]        = user.empleado.estado
            token["es_admin_total"] = user.is_superuser
        return token

    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs)
        if hasattr(self.user, "empleado") and not self.user.empleado.estado:
            raise serializers.ValidationError("Cuenta desactivada. Contacta al administrador.")
        if hasattr(self.user, "empleado"):
            data["empleado"] = {
                "id":           self.user.empleado.id,
                "nombres":      self.user.empleado.nombres,
                "apellidos":    self.user.empleado.apellidos,
                "rol":          self.user.empleado.id_rol.nombre_rol,
                "es_admin_total": self.user.is_superuser,
            }
        return data