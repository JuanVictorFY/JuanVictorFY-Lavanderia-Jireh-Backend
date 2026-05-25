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