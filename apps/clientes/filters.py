import django_filters
from .models import Cliente


class ClienteFilter(django_filters.FilterSet):
    nombres   = django_filters.CharFilter(lookup_expr="icontains")
    apellidos = django_filters.CharFilter(lookup_expr="icontains")
    dni       = django_filters.CharFilter(lookup_expr="icontains")
    correo    = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model  = Cliente
        fields = ["nombres", "apellidos", "dni", "correo"]
