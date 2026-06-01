from django.contrib import admin
from .models import Cliente, PersonaAutorizada


class PersonaAutorizadaInline(admin.TabularInline):
    model  = PersonaAutorizada
    extra  = 0
    fields = ["nombres", "dni", "telefono"]


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display   = ["id", "nombres", "apellidos", "dni", "telefono", "correo", "fecha_registro"]
    search_fields  = ["nombres", "apellidos", "correo", "dni"]
    list_filter    = ["fecha_registro"]
    ordering       = ["apellidos", "nombres"]
    inlines        = [PersonaAutorizadaInline]
    readonly_fields = ["fecha_registro"]


@admin.register(PersonaAutorizada)
class PersonaAutorizadaAdmin(admin.ModelAdmin):
    list_display  = ["id", "nombres", "dni", "telefono", "id_cliente"]
    search_fields = ["nombres", "dni"]
    list_select_related = ["id_cliente"]