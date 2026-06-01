import django_filters
from .models import Pedido


class PedidoFilter(django_filters.FilterSet):
    estado         = django_filters.ChoiceFilter(choices=Pedido.ESTADOS)
    codigo         = django_filters.CharFilter(lookup_expr="icontains")
    fecha_desde    = django_filters.DateTimeFilter(field_name="fecha_ingreso", lookup_expr="gte")
    fecha_hasta    = django_filters.DateTimeFilter(field_name="fecha_ingreso", lookup_expr="lte")
    cliente_nombre = django_filters.CharFilter(
        field_name="id_cliente__nombres", lookup_expr="icontains"
    )

    class Meta:
        model  = Pedido
        fields = ["estado", "codigo", "fecha_desde", "fecha_hasta", "cliente_nombre"]
