from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import EsEmpleadoActivo, EsAdministradorORecepcionista
from .models import Cliente, PersonaAutorizada
from .serializers import ClienteSerializer, PersonaAutorizadaSerializer
from .services import ClienteService


class ClienteViewSet(viewsets.ModelViewSet):
    queryset           = Cliente.objects.prefetch_related("personas_autorizadas").all()
    serializer_class   = ClienteSerializer
    permission_classes = [EsAdministradorORecepcionista]

    # GET /api/clientes/{id}/historial/
    @action(detail=True, methods=["get"], url_path="historial")
    def historial(self, request, pk=None):
        from apps.pedidos.serializers import PedidoSerializer
        data = ClienteService.consultar_historial(pk)
        return Response({
            "cliente": ClienteSerializer(data["cliente"]).data,
            "pedidos": PedidoSerializer(data["pedidos"], many=True).data,
        })

    # POST /api/clientes/{id}/personas-autorizadas/
    @action(detail=True, methods=["post"], url_path="personas-autorizadas")
    def agregar_persona(self, request, pk=None):
        serializer = PersonaAutorizadaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        persona = ClienteService.agregar_persona_autorizada(pk, serializer.validated_data)
        return Response(PersonaAutorizadaSerializer(persona).data, status=201)


class PersonaAutorizadaViewSet(viewsets.ModelViewSet):
    queryset           = PersonaAutorizada.objects.select_related("id_cliente").all()
    serializer_class   = PersonaAutorizadaSerializer
    permission_classes = [EsAdministradorORecepcionista]