from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, PersonaAutorizadaViewSet

router = DefaultRouter()
router.register("",            ClienteViewSet,           basename="clientes")
router.register("autorizadas", PersonaAutorizadaViewSet, basename="autorizadas")

urlpatterns = [path("", include(router.urls))]