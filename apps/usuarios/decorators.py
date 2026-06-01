from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def requiere_rol(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response(
                    {"detail": "No autenticado."}, status=status.HTTP_401_UNAUTHORIZED
                )
            if not hasattr(request.user, "empleado"):
                return Response(
                    {"detail": "No tiene perfil de empleado."}, status=status.HTTP_403_FORBIDDEN
                )
            if request.user.empleado.id_rol.nombre_rol not in roles:
                return Response(
                    {"detail": "No tiene permiso para realizar esta accion."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def requiere_empleado_activo(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "No autenticado."}, status=status.HTTP_401_UNAUTHORIZED
            )
        if not hasattr(request.user, "empleado") or not request.user.empleado.estado:
            return Response(
                {"detail": "Cuenta de empleado inactiva."}, status=status.HTTP_403_FORBIDDEN
            )
        return view_func(request, *args, **kwargs)
    return wrapper
