from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServicioViewSet, DetalleServicioViewSet

router = DefaultRouter()
router.register("",         ServicioViewSet,        basename="servicios")
router.register("detalles", DetalleServicioViewSet, basename="detalles")

urlpatterns = [path("", include(router.urls))]