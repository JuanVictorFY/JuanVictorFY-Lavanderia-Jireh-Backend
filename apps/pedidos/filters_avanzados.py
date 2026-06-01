import django_filters
from .models import Pedido


class PedidoFiltroAvanzado(django_filters.FilterSet):
    estado          = django_filters.ChoiceFilter(choices=Pedido.ESTADOS)
    codigo          = django_filters.CharFilter(lookup_expr="icontains")
    fecha_desde     = django_filters.DateFilter(field_name="fecha_ingreso", lookup_expr="date__gte")
    fecha_hasta     = django_filters.DateFilter(field_name="fecha_ingreso", lookup_expr="date__lte")
    total_min       = django_filters.NumberFilter(field_name="total", lookup_expr="gte")
    total_max       = django_filters.NumberFilter(field_name="total", lookup_expr="lte")
    cliente_dni     = django_filters.CharFilter(field_name="id_cliente__dni", lookup_expr="icontains")
    cliente_nombre  = django_filters.CharFilter(field_name="id_cliente__nombres", lookup_expr="icontains")
    empleado_nombre = django_filters.CharFilter(field_name="id_empleado__nombres", lookup_expr="icontains")
    tiene_pago      = django_filters.BooleanFilter(
        field_name="pagos", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model  = Pedido
        fields = [
            "estado", "codigo", "fecha_desde", "fecha_hasta",
            "total_min", "total_max", "cliente_dni", "cliente_nombre",
            "empleado_nombre", "tiene_pago",
        ]
