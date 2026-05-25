import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response

logger = logging.getLogger("lavanderia")


class ReglaDeNegocioError(Exception):
    pass


class RecursoNoEncontradoError(Exception):
    pass


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ReglaDeNegocioError):
        return Response({"error": str(exc)}, status=400)

    if isinstance(exc, RecursoNoEncontradoError):
        return Response({"error": str(exc)}, status=404)

    if response is None:
        # Error inesperado: solo va al log, nunca se expone al cliente
        logger.error(
            "Error inesperado: %s | Vista: %s",
            str(exc),
            context["view"].__class__.__name__,
            exc_info=True,
        )
        return Response(
            {"error": "Error interno del servidor. Contacte al administrador."},
            status=500,
        )

    logger.warning("Error controlado [%s]: %s", response.status_code, str(exc))
    return response