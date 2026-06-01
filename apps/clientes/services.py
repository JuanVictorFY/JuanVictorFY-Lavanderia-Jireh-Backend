from django.db import transaction
from core.exceptions import RecursoNoEncontradoError, ReglaDeNegocioError
from .models import Cliente, PersonaAutorizada


class ClienteService:

    @staticmethod
    def obtener_o_error(id_cliente: int) -> Cliente:
        try:
            return Cliente.objects.get(pk=id_cliente)
        except Cliente.DoesNotExist:
            raise RecursoNoEncontradoError(f"Cliente {id_cliente} no encontrado.")

    @staticmethod
    def registrar_cliente(datos: dict) -> Cliente:
        correo = datos.get("correo")
        if correo and Cliente.objects.filter(correo=correo).exists():
            raise ReglaDeNegocioError(f"El correo {correo} ya esta en uso.")
        return Cliente.objects.create(**datos)

    @staticmethod
    def consultar_historial(id_cliente: int) -> dict:
        from apps.pedidos.models import Pedido
        cliente = ClienteService.obtener_o_error(id_cliente)
        pedidos = Pedido.objects.filter(id_cliente=cliente).order_by("-fecha_ingreso")
        return {"cliente": cliente, "pedidos": pedidos}

    @staticmethod
    @transaction.atomic
    def agregar_persona_autorizada(id_cliente: int, datos: dict) -> PersonaAutorizada:
        cliente = ClienteService.obtener_o_error(id_cliente)
        dni = datos.get("dni")
        if dni and PersonaAutorizada.objects.filter(dni=dni).exists():
            raise ReglaDeNegocioError(f"Ya existe una persona autorizada con DNI {dni}.")
        return PersonaAutorizada.objects.create(id_cliente=cliente, **datos)

    @staticmethod
    def eliminar_persona_autorizada(id_persona: int) -> None:
        try:
            persona = PersonaAutorizada.objects.get(pk=id_persona)
        except PersonaAutorizada.DoesNotExist:
            raise RecursoNoEncontradoError(f"Persona autorizada {id_persona} no encontrada.")
        persona.delete()