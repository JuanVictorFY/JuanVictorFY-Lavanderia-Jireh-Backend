import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response

logger = logging.getLogger("lavanderia")


class ReglaDeNegocioError(Exception):
    pass


class RecursoNoEncontradoError(Exception):
    pass


class PermisoDenegadoError(Exception):
    pass


class DatosInvalidosError(Exception):
    pass


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ReglaDeNegocioError):
        logger.info("Regla de negocio: %s", str(exc))
        return Response({"error": str(exc)}, status=400)

    if isinstance(exc, RecursoNoEncontradoError):
        logger.info("Recurso no encontrado: %s", str(exc))
        return Response({"error": str(exc)}, status=404)

    if isinstance(exc, PermisoDenegadoError):
        logger.warning("Permiso denegado: %s", str(exc))
        return Response({"error": str(exc)}, status=403)

    if isinstance(exc, DatosInvalidosError):
        return Response({"error": str(exc)}, status=422)

    if response is None:
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