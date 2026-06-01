from rest_framework.response import Response
from rest_framework import status


class SoftDeleteMixin:
    """Mixin para borrado logico marcando campo 'activo' en lugar de eliminar el registro."""

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if hasattr(instance, "estado"):
            instance.estado = False
            instance.save(update_fields=["estado", "updated_at"])
            return Response({"detail": "Registro desactivado."}, status=status.HTTP_200_OK)
        return super().destroy(request, *args, **kwargs)


class OrdenamientoMixin:
    """Expone ordering_fields y ordering por defecto para todos los viewsets."""
    ordering_fields = ["created_at", "updated_at"]
    ordering        = ["-created_at"]


class BusquedaMixin:
    """Agrega search_fields vacio para evitar errores en viewsets sin busqueda configurada."""
    search_fields = []
