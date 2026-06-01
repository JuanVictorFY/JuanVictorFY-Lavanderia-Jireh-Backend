from rest_framework import serializers
from .models import Cliente, PersonaAutorizada


class PersonaAutorizadaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PersonaAutorizada
        fields = ["id", "nombres", "dni", "telefono"]


class ClienteSerializer(serializers.ModelSerializer):
    personas_autorizadas = PersonaAutorizadaSerializer(many=True, read_only=True)

    class Meta:
        model  = Cliente
        fields = [
            "id", "nombres", "apellidos", "dni", "telefono",
            "direccion", "correo", "fecha_registro", "personas_autorizadas"
        ]


class RegistroClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Cliente
        fields = ["nombres", "apellidos", "dni", "telefono", "direccion", "correo"]

    def validate_correo(self, value):
        if value and Cliente.objects.filter(correo=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        return value

    def validate_dni(self, value):
        if value and Cliente.objects.filter(dni=value).exists():
            raise serializers.ValidationError("Este DNI ya está registrado.")
        return value