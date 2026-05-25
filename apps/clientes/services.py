from django.db import transaction
from core.exceptions import RecursoNoEncontradoError
from .models import Cliente, PersonaAutorizada


class ClienteService:

    @staticmethod
    def registrar_cliente(datos: dict) -> Cliente:
        return Cliente.objects.create(**datos)

    @staticmethod
    def consultar_historial(id_cliente: int) -> dict:
        from apps.pedidos.models import Pedido
        try:
            cliente = Cliente.objects.get(pk=id_cliente)
        except Cliente.DoesNotExist:
            raise RecursoNoEncontradoError(f"Cliente {id_cliente} no encontrado.")
        pedidos = Pedido.objects.filter(id_cliente=cliente).order_by("-fecha_ingreso")
        return {"cliente": cliente, "pedidos": pedidos}

    @staticmethod
    @transaction.atomic
    def agregar_persona_autorizada(id_cliente: int, datos: dict) -> PersonaAutorizada:
        try:
            cliente = Cliente.objects.get(pk=id_cliente)
        except Cliente.DoesNotExist:
            raise RecursoNoEncontradoError(f"Cliente {id_cliente} no encontrado.")
        return PersonaAutorizada.objects.create(id_cliente=cliente, **datos)