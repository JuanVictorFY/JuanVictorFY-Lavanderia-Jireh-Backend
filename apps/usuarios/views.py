from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from core.permissions import EsAdministrador, EsEmpleadoActivo
from core.exceptions import ReglaDeNegocioError
from .models import Rol, Empleado
from .serializers import (
    RolSerializer, EmpleadoSerializer,
    CrearEmpleadoSerializer, ActualizarEmpleadoSerializer,
    CambiarContrasenaSerializer, CustomTokenObtainPairSerializer,
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
    search_fields      = ["nombres", "apellidos", "user__username"]
    ordering_fields    = ["apellidos", "nombres", "created_at"]
    ordering           = ["apellidos", "nombres"]
    filterset_fields   = ["estado", "id_rol"]

    def get_serializer_class(self):
        if self.action == "create":
            return CrearEmpleadoSerializer
        if self.action in ["update", "partial_update"]:
            return ActualizarEmpleadoSerializer
        return EmpleadoSerializer

    def _verificar_no_modifica_admin_superior(self, request, empleado_obj):
        """Un admin creado (no superuser) no puede modificar a otro administrador."""
        if request.user.is_superuser:
            return
        if empleado_obj.id_rol.nombre_rol == "administrador" and empleado_obj.user != request.user:
            raise ReglaDeNegocioError("No tienes permiso para modificar a otro administrador.")

    # GET /api/usuarios/empleados/perfil/
    @action(detail=False, methods=["get"], url_path="perfil", permission_classes=[EsEmpleadoActivo])
    def perfil(self, request):
        return Response(EmpleadoSerializer(request.user.empleado).data)

    def create(self, request, *args, **kwargs):
        serializer = CrearEmpleadoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        empleado = serializer.save()
        return Response(EmpleadoSerializer(empleado).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        empleado = self.get_object()
        self._verificar_no_modifica_admin_superior(request, empleado)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        empleado = self.get_object()
        self._verificar_no_modifica_admin_superior(request, empleado)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        empleado = self.get_object()
        self._verificar_no_modifica_admin_superior(request, empleado)
        user = empleado.user
        empleado.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PATCH /api/usuarios/empleados/{id}/cambiar-estado/
    @action(detail=True, methods=["patch"], url_path="cambiar-estado")
    def cambiar_estado(self, request, pk=None):
        empleado_obj = self.get_object()
        self._verificar_no_modifica_admin_superior(request, empleado_obj)
        estado = request.data.get("estado")
        if estado is None:
            return Response({"error": "El campo 'estado' es requerido."}, status=400)
        empleado = EmpleadoService.actualizar_estado(pk, bool(estado))
        return Response(EmpleadoSerializer(empleado).data)

    # PATCH /api/usuarios/empleados/{id}/cambiar-rol/
    @action(detail=True, methods=["patch"], url_path="cambiar-rol")
    def cambiar_rol(self, request, pk=None):
        empleado_obj = self.get_object()
        self._verificar_no_modifica_admin_superior(request, empleado_obj)
        id_rol = request.data.get("id_rol")
        if not id_rol:
            return Response({"error": "El campo 'id_rol' es requerido."}, status=400)
        empleado = EmpleadoService.cambiar_rol(pk, id_rol)
        return Response(EmpleadoSerializer(empleado).data)

    # PATCH /api/usuarios/empleados/{id}/cambiar-contrasena/
    @action(detail=True, methods=["patch"], url_path="cambiar-contrasena")
    def cambiar_contrasena(self, request, pk=None):
        empleado_obj = self.get_object()
        self._verificar_no_modifica_admin_superior(request, empleado_obj)
        serializer = CambiarContrasenaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        empleado = EmpleadoService.cambiar_contrasena(pk, serializer.validated_data["nueva_contrasena"])
        return Response(EmpleadoSerializer(empleado).data)