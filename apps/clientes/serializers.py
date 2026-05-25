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
            "id", "nombres", "apellidos", "telefono",
            "direccion", "correo", "fecha_registro", "personas_autorizadas"
        ]