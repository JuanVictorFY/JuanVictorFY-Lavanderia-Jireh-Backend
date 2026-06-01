from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from apps.usuarios.views import CustomTokenObtainPairView
from apps.pedidos.views import ConsultaPedidoPublicaView


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        "api": "Lavanderia Jireh API",
        "version": "1.0",
        "endpoints": {
            "auth":      "/api/auth/",
            "usuarios":  "/api/usuarios/",
            "clientes":  "/api/clientes/",
            "pedidos":   "/api/pedidos/",
            "servicios": "/api/servicios/",
            "pagos":     "/api/pagos/",
            "reportes":  "/api/reportes/",
            "admin":     "/admin/",
        }
    })


urlpatterns = [
    path("", api_root),
    path("admin/", admin.site.urls),

    # Auth JWT
    path("api/auth/login/",   CustomTokenObtainPairView.as_view(), name="token_obtain"),
    path("api/auth/refresh/", TokenRefreshView.as_view(),          name="token_refresh"),
    path("api/auth/logout/",  TokenBlacklistView.as_view(),        name="token_blacklist"),

    # Apps
    path("api/usuarios/",  include("apps.usuarios.urls")),
    path("api/clientes/",  include("apps.clientes.urls")),
    path("api/pedidos/",   include("apps.pedidos.urls")),
    path("api/servicios/", include("apps.servicios.urls")),
    path("api/pagos/",     include("apps.pagos.urls")),
    path("api/reportes/",  include("apps.reportes.urls")),

    # Consulta pública — sin token
    path("pedido/<str:codigo>/", ConsultaPedidoPublicaView.as_view(), name="consulta-publica"),
]