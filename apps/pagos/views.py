from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import EsAdministradorORecepcionista
from .models import Pago
from .serializers import PagoSerializer
from .services import PagoService


class PagoViewSet(viewsets.ModelViewSet):
    queryset           = Pago.objects.select_related("id_pedido").all()
    serializer_class   = PagoSerializer
    permission_classes = [EsAdministradorORecepcionista]

    def create(self, request, *args, **kwargs):
        id_pedido   = request.data.get("id_pedido")
        monto       = request.data.get("monto")
        metodo_pago = request.data.get("metodo_pago")
        pago = PagoService.registrar_pago(id_pedido, monto, metodo_pago)
        return Response(PagoSerializer(pago).data, status=201)

    # PATCH /api/pagos/{id}/anular/
    @action(detail=True, methods=["patch"], url_path="anular")
    def anular(self, request, pk=None):
        pago = PagoService.anular_pago(pk)
        return Response(PagoSerializer(pago).data)