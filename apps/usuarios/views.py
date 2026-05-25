from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from core.permissions import EsAdministrador, EsEmpleadoActivo
from .models import Rol, Empleado
from .serializers import (
    RolSerializer, EmpleadoSerializer,
    CrearEmpleadoSerializer, ActualizarEmpleadoSerializer,
    CustomTokenObtainPairSerializer,
)
from .services import EmpleadoService


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RolViewSet(viewsets.ModelViewSet):
    queryset           = Rol.objects.all()
    serializer_class   = RolSerializer
    permission_classes = [EsAdministrador]


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset           = Empleado.objects.select_related("id_rol", "user").all()
    permission_classes = [EsAdministrador]

    def get_serializer_class(self):
        if self.action == "create":
            return CrearEmpleadoSerializer
        if self.action in ["update", "partial_update"]:
            return ActualizarEmpleadoSerializer
        return EmpleadoSerializer

    # GET /api/usuarios/empleados/perfil/
    @action(detail=False, methods=["get"], url_path="perfil", permission_classes=[EsEmpleadoActivo])
    def perfil(self, request):
        return Response(EmpleadoSerializer(request.user.empleado).data)

    # PATCH /api/usuarios/empleados/{id}/cambiar-estado/
    @action(detail=True, methods=["patch"], url_path="cambiar-estado")
    def cambiar_estado(self, request, pk=None):
        estado = request.data.get("estado")
        if estado is None:
            return Response({"error": "El campo 'estado' es requerido."}, status=400)
        empleado = EmpleadoService.actualizar_estado(pk, bool(estado))
        return Response(EmpleadoSerializer(empleado).data)

    # PATCH /api/usuarios/empleados/{id}/cambiar-rol/
    @action(detail=True, methods=["patch"], url_path="cambiar-rol")
    def cambiar_rol(self, request, pk=None):
        id_rol = request.data.get("id_rol")
        if not id_rol:
            return Response({"error": "El campo 'id_rol' es requerido."}, status=400)
        empleado = EmpleadoService.cambiar_rol(pk, id_rol)
        return Response(EmpleadoSerializer(empleado).data)