from django.contrib import admin
from .models import Rol, Empleado


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display  = ["id", "nombre_rol", "created_at"]
    search_fields = ["nombre_rol"]
    ordering      = ["nombre_rol"]


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display        = ["id", "nombres", "apellidos", "id_rol", "telefono", "estado", "created_at"]
    list_filter         = ["estado", "id_rol"]
    search_fields       = ["nombres", "apellidos", "user__username"]
    list_editable       = ["estado"]
    list_select_related = ["id_rol", "user"]
    readonly_fields     = ["created_at", "updated_at"]
    fieldsets = (
        ("Datos personales", {"fields": ("nombres", "apellidos", "telefono")}),
        ("Cuenta y rol",     {"fields": ("user", "id_rol", "estado")}),
        ("Timestamps",       {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )