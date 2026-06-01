from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import EsAdministradorORecepcionista
from core.exceptions import RecursoNoEncontradoError
from .models import Servicio, DetalleServicio
from .serializers import ServicioSerializer, DetalleServicioSerializer
from .services import ServicioService


class ServicioViewSet(viewsets.ModelViewSet):
    queryset           = Servicio.objects.all()
    serializer_class   = ServicioSerializer
    permission_classes = [EsAdministradorORecepcionista]
    search_fields      = ["nombre_servicio"]
    ordering_fields    = ["nombre_servicio", "precio_base"]
    ordering           = ["nombre_servicio"]


class DetalleServicioViewSet(viewsets.ModelViewSet):
    queryset           = DetalleServicio.objects.select_related("id_prenda", "id_servicio").all()
    serializer_class   = DetalleServicioSerializer
    permission_classes = [EsAdministradorORecepcionista]

    @action(detail=False, methods=["post"], url_path="calcular")
    def calcular(self, request):
        id_prenda   = request.data.get("id_prenda")
        id_servicio = request.data.get("id_servicio")
        if not id_prenda or not id_servicio:
            return Response(
                {"detail": "Se requieren id_prenda e id_servicio."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            detalle = ServicioService.calcular_subtotal(id_prenda, id_servicio)
        except RecursoNoEncontradoError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(DetalleServicioSerializer(detalle).data, status=status.HTTP_201_CREATED)