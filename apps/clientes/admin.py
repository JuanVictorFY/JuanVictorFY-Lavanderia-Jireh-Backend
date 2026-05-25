from django.contrib import admin
from .models import Cliente, PersonaAutorizada


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ["id", "nombres", "apellidos", "telefono", "correo"]
    search_fields = ["nombres", "apellidos", "correo"]


@admin.register(PersonaAutorizada)
class PersonaAutorizadaAdmin(admin.ModelAdmin):
    list_display  = ["id", "nombres", "dni", "id_cliente"]
    search_fields = ["nombres", "dni"]