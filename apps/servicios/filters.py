import django_filters
from .models import Servicio


class ServicioFilter(django_filters.FilterSet):
    nombre_servicio = django_filters.CharFilter(lookup_expr="icontains")
    precio_min      = django_filters.NumberFilter(field_name="precio_base", lookup_expr="gte")
    precio_max      = django_filters.NumberFilter(field_name="precio_base", lookup_expr="lte")

    class Meta:
        model  = Servicio
        fields = ["nombre_servicio", "precio_min", "precio_max"]
