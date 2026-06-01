import logging

logger = logging.getLogger("lavanderia")


class AuditoriaEmpleadoMiddleware:
    """Registra en log las solicitudes autenticadas indicando el empleado y rol."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and hasattr(request.user, "empleado"):
            emp = request.user.empleado
            logger.debug(
                "[AUDITORIA] %s %s — empleado: %s (%s) — status: %s",
                request.method,
                request.path,
                emp,
                emp.id_rol.nombre_rol,
                response.status_code,
            )
        return response
