import django_filters
from .models import Empleado


class EmpleadoFilter(django_filters.FilterSet):
    nombres   = django_filters.CharFilter(lookup_expr="icontains")
    apellidos = django_filters.CharFilter(lookup_expr="icontains")
    estado    = django_filters.BooleanFilter()
    rol       = django_filters.CharFilter(field_name="id_rol__nombre_rol", lookup_expr="icontains")

    class Meta:
        model  = Empleado
        fields = ["nombres", "apellidos", "estado", "rol"]
