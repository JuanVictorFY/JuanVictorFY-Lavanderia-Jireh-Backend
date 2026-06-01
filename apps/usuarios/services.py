from django.contrib.auth.models import User
from django.db import transaction
from core.exceptions import ReglaDeNegocioError, RecursoNoEncontradoError
from .models import Empleado, Rol


class EmpleadoService:

    @staticmethod
    @transaction.atomic
    def crear_empleado(usuario: str, contrasena: str, nombres: str,
                       apellidos: str, id_rol: Rol, telefono: str = "") -> Empleado:
        user = User.objects.create_user(username=usuario, password=contrasena)
        return Empleado.objects.create(
            user=user, id_rol=id_rol, nombres=nombres,
            apellidos=apellidos, telefono=telefono, estado=True,
        )

    @staticmethod
    def actualizar_estado(id_empleado: int, estado: bool) -> Empleado:
        try:
            empleado = Empleado.objects.get(pk=id_empleado)
        except Empleado.DoesNotExist:
            raise RecursoNoEncontradoError(f"Empleado {id_empleado} no encontrado.")
        empleado.estado = estado
        empleado.save(update_fields=["estado", "updated_at"])
        return empleado

    @staticmethod
    def cambiar_contrasena(id_empleado: int, nueva_contrasena: str) -> Empleado:
        try:
            empleado = Empleado.objects.select_related("user").get(pk=id_empleado)
        except Empleado.DoesNotExist:
            raise RecursoNoEncontradoError(f"Empleado {id_empleado} no encontrado.")
        empleado.user.set_password(nueva_contrasena)
        empleado.user.save(update_fields=["password"])
        return empleado

    @staticmethod
    def cambiar_rol(id_empleado: int, id_rol: int) -> Empleado:
        try:
            empleado = Empleado.objects.get(pk=id_empleado)
            rol      = Rol.objects.get(pk=id_rol)
        except Empleado.DoesNotExist:
            raise RecursoNoEncontradoError(f"Empleado {id_empleado} no encontrado.")
        except Rol.DoesNotExist:
            raise RecursoNoEncontradoError(f"Rol {id_rol} no encontrado.")
        empleado.id_rol = rol
        empleado.save(update_fields=["id_rol", "updated_at"])
        return empleado