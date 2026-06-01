from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Ejecuta todos los comandos de seed en el orden correcto"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("== Iniciando seed completo =="))
        pasos = [
            ("seed_roles",    "Roles"),
            ("seed_servicios","Servicios"),
            ("seed_clientes", "Clientes"),
            ("seed_pedidos",  "Pedidos"),
            ("seed_pagos",    "Pagos"),
        ]
        for comando, descripcion in pasos:
            self.stdout.write(f"  → Ejecutando {descripcion}...")
            try:
                call_command(comando, verbosity=0)
                self.stdout.write(self.style.SUCCESS(f"    ✓ {descripcion} completado."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"    ✗ Error en {descripcion}: {e}"))

        self.stdout.write(self.style.SUCCESS("== Seed completo finalizado =="))
