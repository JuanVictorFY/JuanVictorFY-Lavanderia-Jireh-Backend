from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RolViewSet, EmpleadoViewSet

router = DefaultRouter()
router.register("roles",     RolViewSet,      basename="roles")
router.register("empleados", EmpleadoViewSet, basename="empleados")

urlpatterns = [path("", include(router.urls))]