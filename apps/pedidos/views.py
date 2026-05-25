from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.permissions import EsEmpleadoActivo
from core.exceptions import RecursoNoEncontradoError
from .models import Pedido
from .serializers import PedidoSerializer, CrearPedidoSerializer, EstadoPedidoSerializer
from .services import PedidoService


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.select_related(
        "id_cliente", "id_empleado"
    ).prefetch_related("prendas", "estados").all()
    permission_classes = [EsEmpleadoActivo]

    def get_serializer_class(self):
        if self.action == "create":
            return CrearPedidoSerializer
        return PedidoSerializer

    def create(self, request, *args, **kwargs):
        serializer = CrearPedidoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pedido = serializer.save()
        return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)

    # PATCH /api/pedidos/{id}/cambiar-estado/
    @action(detail=True, methods=["patch"], url_path="cambiar-estado")
    def cambiar_estado(self, request, pk=None):
        nuevo_estado = request.data.get("estado")
        descripcion  = request.data.get("descripcion", "")
        estado_obj   = PedidoService.cambiar_estado(pk, nuevo_estado, descripcion)
        return Response(EstadoPedidoSerializer(estado_obj).data)

    # POST /api/pedidos/{id}/calcular-total/
    @action(detail=True, methods=["post"], url_path="calcular-total")
    def calcular_total(self, request, pk=None):
        pedido = PedidoService.obtener_pedido_por_id(pk)
        total  = PedidoService.calcular_total(pedido)
        return Response({"total": str(total)})


# URL pública — sin token requerido 
class ConsultaPedidoPublicaView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, codigo=None):
        try:
            data = PedidoService.obtener_pedido_por_codigo(codigo)
        except RecursoNoEncontradoError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(data)