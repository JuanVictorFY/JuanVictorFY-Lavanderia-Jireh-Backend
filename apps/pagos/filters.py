import django_filters
from .models import Pago


class PagoFilter(django_filters.FilterSet):
    metodo_pago = django_filters.ChoiceFilter(choices=Pago.METODOS)
    estado_pago = django_filters.ChoiceFilter(choices=Pago.ESTADOS_PAGO)
    fecha_desde = django_filters.DateTimeFilter(field_name="fecha_pago", lookup_expr="gte")
    fecha_hasta = django_filters.DateTimeFilter(field_name="fecha_pago", lookup_expr="lte")
    monto_min   = django_filters.NumberFilter(field_name="monto", lookup_expr="gte")
    monto_max   = django_filters.NumberFilter(field_name="monto", lookup_expr="lte")

    class Meta:
        model  = Pago
        fields = ["metodo_pago", "estado_pago", "fecha_desde", "fecha_hasta", "monto_min", "monto_max"]
