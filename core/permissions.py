from rest_framework.permissions import BasePermission


class EsAdministrador(BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated
            and hasattr(request.user, "empleado")
            and request.user.empleado.id_rol.nombre_rol == "administrador"
        )


class EsEmpleadoActivo(BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated
            and hasattr(request.user, "empleado")
            and request.user.empleado.estado is True
        )


class EsAdministradorORecepcionista(BasePermission):
    """Bloquea a operarios — solo admin y recepcionista pasan."""
    def has_permission(self, request, view) -> bool:
        if not (request.user.is_authenticated and hasattr(request.user, "empleado")):
            return False
        rol = request.user.empleado.id_rol.nombre_rol
        return rol in ("administrador", "recepcionista")