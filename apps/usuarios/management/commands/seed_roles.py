from django.core.management.base import BaseCommand
from apps.usuarios.models import Rol


ROLES = ["administrador", "recepcionista", "operario", "cajero"]


class Command(BaseCommand):
    help = "Crea los roles basicos del sistema si no existen"

    def handle(self, *args, **options):
        creados = 0
        for nombre in ROLES:
            _, created = Rol.objects.get_or_create(nombre_rol=nombre)
            if created:
                creados += 1
        self.stdout.write(self.style.SUCCESS(f"{creados} roles creados. Total: {Rol.objects.count()}"))
