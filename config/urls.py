from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from apps.usuarios.views import CustomTokenObtainPairView
from apps.pedidos.views import ConsultaPedidoPublicaView


urlpatterns = [
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

    # Consulta pública — sin token
    path("pedido/<str:codigo>/", ConsultaPedidoPublicaView.as_view(), name="consulta-publica"),
]