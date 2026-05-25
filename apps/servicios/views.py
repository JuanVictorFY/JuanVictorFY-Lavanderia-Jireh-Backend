from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import EsEmpleadoActivo, EsAdministrador
from .models import Servicio, DetalleServicio
from .serializers import ServicioSerializer, DetalleServicioSerializer
from .services import ServicioService


class ServicioViewSet(viewsets.ModelViewSet):
    queryset           = Servicio.objects.all()
    serializer_class   = ServicioSerializer
    permission_classes = [EsEmpleadoActivo]


class DetalleServicioViewSet(viewsets.ModelViewSet):
    queryset           = DetalleServicio.objects.select_related("id_prenda", "id_servicio").all()
    serializer_class   = DetalleServicioSerializer
    permission_classes = [EsEmpleadoActivo]

    # POST /api/servicios/detalles/calcular/
    @action(detail=False, methods=["post"], url_path="calcular")
    def calcular(self, request):
        id_prenda   = request.data.get("id_prenda")
        id_servicio = request.data.get("id_servicio")
        detalle     = ServicioService.calcular_subtotal(id_prenda, id_servicio)
        return Response(DetalleServicioSerializer(detalle).data, status=201)