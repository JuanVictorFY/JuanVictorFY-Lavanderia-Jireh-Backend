from django.core.management.base import BaseCommand
from apps.clientes.models import Cliente


CLIENTES_DEMO = [
    ("Maria", "Quispe Flores",    "12345678", "987654321", "Av. Los Olivos 123",   "maria.quispe@email.com"),
    ("Juan",  "Mamani Torres",    "23456789", "976543210", "Jr. Lima 456",         "juan.mamani@email.com"),
    ("Rosa",  "Condori Apaza",    "34567890", "965432109", "Calle Arequipa 789",   "rosa.condori@email.com"),
    ("Luis",  "Huanca Catari",    "45678901", "954321098", "Av. Ejercito 321",     "luis.huanca@email.com"),
    ("Ana",   "Vargas Mendoza",   "56789012", "943210987", "Jr. Puno 654",         "ana.vargas@email.com"),
    ("Pedro", "Llanqui Choqque",  "67890123", "932109876", "Av. Tacna 987",        "pedro.llanqui@email.com"),
    ("Elena", "Ramos Salas",      "78901234", "921098765", "Calle Moquegua 159",   "elena.ramos@email.com"),
    ("Carlos","Flores Mamani",    "89012345", "910987654", "Jr. Cusco 753",        "carlos.flores@email.com"),
    ("Sofia", "Torres Quispe",    "90123456", "909876543", "Av. San Martin 246",   "sofia.torres@email.com"),
    ("Diego", "Apaza Larico",     "01234567", "898765432", "Calle Bolivar 135",    "diego.apaza@email.com"),
]


class Command(BaseCommand):
    help = "Carga clientes de demostracion en la base de datos"

    def handle(self, *args, **options):
        creados = 0
        for nombres, apellidos, dni, telefono, direccion, correo in CLIENTES_DEMO:
            _, created = Cliente.objects.get_or_create(
                correo=correo,
                defaults={
                    "nombres": nombres,
                    "apellidos": apellidos,
                    "dni": dni,
                    "telefono": telefono,
                    "direccion": direccion,
                },
            )
            if created:
                creados += 1
        self.stdout.write(self.style.SUCCESS(f"{creados} clientes demo creados."))
