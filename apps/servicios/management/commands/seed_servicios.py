from django.core.management.base import BaseCommand
from apps.servicios.models import Servicio
from decimal import Decimal


SERVICIOS_INICIALES = [
    ("Lavado Normal",        "Lavado y secado estandar de ropa.",           Decimal("12.00")),
    ("Lavado Delicado",      "Para prendas delicadas: seda, lana, lycra.",  Decimal("20.00")),
    ("Lavado Express",       "Servicio rapido en menos de 4 horas.",        Decimal("25.00")),
    ("Planchado Simple",     "Planchado basico de prendas livianas.",       Decimal("8.00")),
    ("Planchado Profesional","Planchado de camisas, ternos y uniformes.",   Decimal("15.00")),
    ("Lavado de Edredon",    "Lavado de edredones y colchas grandes.",      Decimal("35.00")),
    ("Lavado de Cortinas",   "Lavado y planchado de cortinas.",             Decimal("30.00")),
    ("Lavado de Zapatos",    "Limpieza y desinfeccion de calzado.",         Decimal("18.00")),
    ("Dry Cleaning",         "Limpieza en seco para prendas especiales.",   Decimal("40.00")),
    ("Lavado + Planchado",   "Servicio completo de lavado y planchado.",    Decimal("22.00")),
]


class Command(BaseCommand):
    help = "Carga servicios iniciales en la base de datos"

    def add_arguments(self, parser):
        parser.add_argument("--flush", action="store_true", help="Eliminar servicios existentes antes de cargar")

    def handle(self, *args, **options):
        if options["flush"]:
            Servicio.objects.all().delete()
            self.stdout.write(self.style.WARNING("Servicios eliminados."))

        creados = 0
        for nombre, descripcion, precio in SERVICIOS_INICIALES:
            obj, created = Servicio.objects.get_or_create(
                nombre_servicio=nombre,
                defaults={"descripcion": descripcion, "precio_base": precio},
            )
            if created:
                creados += 1

        self.stdout.write(self.style.SUCCESS(f"{creados} servicios creados correctamente."))
