from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from core.permissions import EsEmpleadoActivo
from .models import Cliente
from .serializers import ClienteSerializer
from .filters import ClienteFilter


@api_view(["GET"])
@permission_classes([EsEmpleadoActivo])
def buscar_clientes(request):
    """Busqueda rapida de clientes por nombre, apellido o DNI."""
    q = request.query_params.get("q", "").strip()
    if len(q) < 2:
        return Response({"detail": "La busqueda debe tener al menos 2 caracteres."}, status=400)

    clientes = Cliente.objects.filter(
        nombres__icontains=q
    ) | Cliente.objects.filter(
        apellidos__icontains=q
    ) | Cliente.objects.filter(
        dni__icontains=q
    )
    clientes = clientes.distinct().order_by("apellidos", "nombres")[:20]
    return Response(ClienteSerializer(clientes, many=True).data)


@api_view(["GET"])
@permission_classes([EsEmpleadoActivo])
def estadisticas_cliente(request, pk):
    """Devuelve estadisticas basicas de un cliente."""
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response({"detail": "Cliente no encontrado."}, status=404)

    from apps.pedidos.models import Pedido
    pedidos = cliente.pedidos.all()
    return Response({
        "cliente":             str(cliente),
        "total_pedidos":       pedidos.count(),
        "pedidos_entregados":  pedidos.filter(estado=Pedido.ENTREGADO).count(),
        "pedidos_pendientes":  pedidos.filter(estado=Pedido.PENDIENTE).count(),
        "gasto_total":         str(sum(p.total for p in pedidos)),
    })
