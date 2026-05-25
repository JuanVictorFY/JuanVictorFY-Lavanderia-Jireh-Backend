from django.contrib import admin
from .models import Rol, Empleado


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display  = ["id", "nombre_rol", "created_at"]
    search_fields = ["nombre_rol"]


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display  = ["id", "nombres", "apellidos", "id_rol", "estado"]
    list_filter   = ["estado", "id_rol"]
    search_fields = ["nombres", "apellidos", "user__username"]
    list_editable = ["estado"]