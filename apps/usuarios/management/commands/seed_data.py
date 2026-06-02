from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import datetime

from apps.usuarios.models import Rol, Empleado
from apps.clientes.models import Cliente, PersonaAutorizada
from apps.servicios.models import Servicio, DetalleServicio
from apps.pedidos.models import Pedido, Prenda, EstadoPedido
from apps.pagos.models import Pago


class Command(BaseCommand):
    help = "Pobla la base de datos con datos de ejemplo"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creando datos de ejemplo...")

        self._crear_roles()
        self._crear_usuarios()
        self._crear_clientes()
        self._crear_servicios()
        self._crear_pedidos()

        self.stdout.write(self.style.SUCCESS("Datos creados exitosamente."))

    # ------------------------------------------------------------------
    def _crear_roles(self):
        roles = ["Administrador", "Recepcionista", "Lavandero"]
        for nombre in roles:
            Rol.objects.get_or_create(nombre_rol=nombre)
        self.stdout.write("  Roles listos.")

    # ------------------------------------------------------------------
    def _crear_usuarios(self):
        rol_admin = Rol.objects.get(nombre_rol="Administrador")
        rol_recep = Rol.objects.get(nombre_rol="Recepcionista")
        rol_lava  = Rol.objects.get(nombre_rol="Lavandero")

        usuarios = [
            {
                "username": "admin",
                "email":    "admin@lavanderia.com",
                "password": "12345678",
                "nombres":  "Juan",
                "apellidos":"Pérez Torres",
                "telefono": "987654321",
                "is_staff": True,
                "is_superuser": True,
                "rol": rol_admin,
            },
            {
                "username": "maria_r",
                "email":    "maria@lavanderia.com",
                "password": "Recep456!",
                "nombres":  "María",
                "apellidos":"Ríos Salinas",
                "telefono": "976543210",
                "is_staff": True,
                "is_superuser": True,
                "rol": rol_recep,
            },
            {
                "username": "carlos_m",
                "email":    "carlos@lavanderia.com",
                "password": "Lava789!",
                "nombres":  "Carlos",
                "apellidos":"Mamani Quispe",
                "telefono": "965432109",
                "is_staff": True,
                "is_superuser": True,
                "rol": rol_lava,
            },
        ]

        for datos in usuarios:
            user, created = User.objects.get_or_create(
                username=datos["username"],
                defaults={
                    "email":        datos["email"],
                    "is_staff":     datos["is_staff"],
                    "is_superuser": datos["is_superuser"],
                },
            )
            if created:
                user.set_password(datos["password"])
                user.save()

            Empleado.objects.get_or_create(
                user=user,
                defaults={
                    "id_rol":    datos["rol"],
                    "nombres":   datos["nombres"],
                    "apellidos": datos["apellidos"],
                    "telefono":  datos["telefono"],
                    "estado":    True,
                },
            )

        self.stdout.write("  Usuarios y empleados listos.")
        self.stdout.write("    admin     / 12345678")
        self.stdout.write("    maria_r   / Recep456!")
        self.stdout.write("    carlos_m  / Lava789!")

    # ------------------------------------------------------------------
    def _crear_clientes(self):
        clientes_data = [
            ("Ana",     "García López",   "74521896", "991234567", "Av. Grau 123",        "ana.garcia@gmail.com"),
            ("Luis",    "Torres Ramos",   "63489512", "982345678", "Jr. Lima 456",        "luis.torres@hotmail.com"),
            ("Carmen",  "Huanca Flores",  "52378964", "973456789", "Calle Real 789",      "carmen.huanca@gmail.com"),
            ("Roberto", "Chávez Mendoza", "41267853", "964567890", "Av. Bolívar 321",     "roberto.chavez@yahoo.com"),
            ("Sandra",  "Condori Vargas", "30156742", "955678901", "Jr. Ayacucho 654",    None),
            ("Miguel",  "Quispe Apaza",   "29045631", "946789012", "Psje. Los Pinos 11",  "miguel.quispe@gmail.com"),
            ("Rosa",    "Mamani Cjuno",   "18934520", "937890123", "Av. 28 de Julio 88",  None),
            ("Diego",   "Paredes Salas",  "07823419", "928901234", "Calle Dos de Mayo 5", "diego.paredes@gmail.com"),
        ]

        clientes = []
        for nombres, apellidos, dni, telefono, direccion, correo in clientes_data:
            cliente, _ = Cliente.objects.get_or_create(
                dni=dni,
                defaults={
                    "nombres":   nombres,
                    "apellidos": apellidos,
                    "telefono":  telefono,
                    "direccion": direccion,
                    "correo":    correo,
                },
            )
            clientes.append(cliente)

        PersonaAutorizada.objects.get_or_create(
            dni="85631247",
            defaults={"id_cliente": clientes[0], "nombres": "Pedro García",  "telefono": "991111222"},
        )
        PersonaAutorizada.objects.get_or_create(
            dni="74520136",
            defaults={"id_cliente": clientes[2], "nombres": "Jorge Huanca",  "telefono": "982222333"},
        )
        PersonaAutorizada.objects.get_or_create(
            dni="63419025",
            defaults={"id_cliente": clientes[4], "nombres": "Lucía Condori", "telefono": "973333444"},
        )

        self.stdout.write("  Clientes listos.")
        return clientes

    # ------------------------------------------------------------------
    def _crear_servicios(self):
        servicios_data = [
            ("Lavado Normal",       "Lavado estándar de ropa en general",                    Decimal("8.00")),
            ("Lavado Delicado",     "Lavado especial para prendas delicadas o de lana",      Decimal("12.00")),
            ("Lavado en Seco",      "Limpieza en seco para ropa formal y trajes",            Decimal("25.00")),
            ("Planchado",           "Servicio de planchado por prenda",                      Decimal("3.50")),
            ("Lavado + Planchado",  "Lavado completo más planchado incluido",                Decimal("14.00")),
            ("Desinfección",        "Lavado con tratamiento antibacterial y desinfectante",  Decimal("15.00")),
            ("Lavado de Edredón",   "Lavado especial para edredones y cobertores",           Decimal("30.00")),
            ("Lavado de Zapatillas","Limpieza de zapatillas a mano y secado",               Decimal("18.00")),
        ]

        for nombre, descripcion, precio in servicios_data:
            Servicio.objects.get_or_create(
                nombre_servicio=nombre,
                defaults={"descripcion": descripcion, "precio_base": precio},
            )

        self.stdout.write("  Servicios listos.")

    # ------------------------------------------------------------------
    def _crear_pedidos(self):
        if Pedido.objects.exists():
            self.stdout.write("  Pedidos ya existen, se omite.")
            return

        clientes  = list(Cliente.objects.all())
        empleado  = Empleado.objects.get(user__username="maria_r")
        svc       = {s.nombre_servicio: s for s in Servicio.objects.all()}

        ahora = timezone.now()

        pedidos_data = [
            {
                "cliente": clientes[0], "estado": Pedido.ENTREGADO,
                "fecha_ingreso": ahora - datetime.timedelta(days=6),
                "fecha_entrega": ahora - datetime.timedelta(days=4),
                "observaciones": None,
                "prendas": [
                    {"tipo": "Camisa",   "color": "Blanco", "peso": 0.30, "cantidad": 3, "servicio": "Lavado + Planchado", "subtotal": 14.00},
                    {"tipo": "Pantalón", "color": "Azul",   "peso": 0.60, "cantidad": 2, "servicio": "Lavado + Planchado", "subtotal": 28.00},
                ],
                "pago": {"monto": 45.50, "metodo": Pago.EFECTIVO, "estado": Pago.PAGADO},
            },
            {
                "cliente": clientes[1], "estado": Pedido.ENTREGADO,
                "fecha_ingreso": ahora - datetime.timedelta(days=5),
                "fecha_entrega": ahora - datetime.timedelta(days=3),
                "observaciones": "Cliente pidió fragancia",
                "prendas": [
                    {"tipo": "Polo", "color": "Verde", "peso": 0.25, "cantidad": 4, "servicio": "Lavado Normal", "subtotal": 28.00},
                ],
                "pago": {"monto": 28.00, "metodo": Pago.YAPE, "estado": Pago.PAGADO},
            },
            {
                "cliente": clientes[2], "estado": Pedido.LISTO,
                "fecha_ingreso": ahora - datetime.timedelta(days=4),
                "fecha_entrega": ahora - datetime.timedelta(days=2),
                "observaciones": None,
                "prendas": [
                    {"tipo": "Traje",   "color": "Negro",   "peso": 1.20, "cantidad": 1, "servicio": "Lavado en Seco",    "subtotal": 25.00},
                    {"tipo": "Camisa",  "color": "Celeste", "peso": 0.30, "cantidad": 3, "servicio": "Lavado + Planchado","subtotal": 14.00},
                    {"tipo": "Edredón", "color": "Beige",   "peso": 2.50, "cantidad": 1, "servicio": "Lavado de Edredón", "subtotal": 30.00},
                ],
                "pago": {"monto": 62.00, "metodo": Pago.TRANSFERENCIA, "estado": Pago.PENDIENTE},
            },
            {
                "cliente": clientes[3], "estado": Pedido.EN_PROCESO,
                "fecha_ingreso": ahora - datetime.timedelta(days=3),
                "fecha_entrega": ahora - datetime.timedelta(days=1),
                "observaciones": "Mancha difícil en camisa",
                "prendas": [
                    {"tipo": "Camisa", "color": "Blanco", "peso": 0.30, "cantidad": 2, "servicio": "Lavado Normal", "subtotal": 16.00},
                    {"tipo": "Jean",   "color": "Azul",   "peso": 0.80, "cantidad": 1, "servicio": "Lavado Normal", "subtotal":  8.00},
                ],
                "pago": {"monto": 33.50, "metodo": Pago.EFECTIVO, "estado": Pago.PENDIENTE},
            },
            {
                "cliente": clientes[4], "estado": Pedido.EN_PROCESO,
                "fecha_ingreso": ahora - datetime.timedelta(days=2),
                "fecha_entrega": ahora + datetime.timedelta(days=1),
                "observaciones": None,
                "prendas": [
                    {"tipo": "Ropa de cama", "color": "Blanco", "peso": 3.00, "cantidad": 2, "servicio": "Desinfección", "subtotal": 30.00},
                ],
                "pago": {"monto": 55.00, "metodo": Pago.TARJETA, "estado": Pago.PENDIENTE},
            },
            {
                "cliente": clientes[5], "estado": Pedido.PENDIENTE,
                "fecha_ingreso": ahora - datetime.timedelta(days=1),
                "fecha_entrega": ahora + datetime.timedelta(days=2),
                "observaciones": None,
                "prendas": [
                    {"tipo": "Zapatillas", "color": "Blanco", "peso": 0.90, "cantidad": 1, "servicio": "Lavado de Zapatillas", "subtotal": 18.00},
                ],
                "pago": None,
            },
            {
                "cliente": clientes[6], "estado": Pedido.PENDIENTE,
                "fecha_ingreso": ahora,
                "fecha_entrega": ahora + datetime.timedelta(days=3),
                "observaciones": "Edredón doble",
                "prendas": [
                    {"tipo": "Edredón", "color": "Gris", "peso": 3.50, "cantidad": 1, "servicio": "Lavado de Edredón", "subtotal": 30.00},
                ],
                "pago": None,
            },
            {
                "cliente": clientes[7], "estado": Pedido.PENDIENTE,
                "fecha_ingreso": ahora,
                "fecha_entrega": ahora + datetime.timedelta(days=3),
                "observaciones": None,
                "prendas": [
                    {"tipo": "Polo",  "color": "Rojo",  "peso": 0.25, "cantidad": 2, "servicio": "Lavado Normal", "subtotal": 16.00},
                    {"tipo": "Short", "color": "Negro", "peso": 0.35, "cantidad": 2, "servicio": "Lavado Normal", "subtotal":  7.00},
                ],
                "pago": None,
            },
        ]

        estados_historial = {
            Pedido.ENTREGADO:  [Pedido.PENDIENTE, Pedido.EN_PROCESO, Pedido.LISTO, Pedido.ENTREGADO],
            Pedido.LISTO:      [Pedido.PENDIENTE, Pedido.EN_PROCESO, Pedido.LISTO],
            Pedido.EN_PROCESO: [Pedido.PENDIENTE, Pedido.EN_PROCESO],
            Pedido.PENDIENTE:  [Pedido.PENDIENTE],
        }

        for datos in pedidos_data:
            total = sum(Decimal(str(p["subtotal"])) for p in datos["prendas"])

            pedido = Pedido.objects.create(
                id_cliente=datos["cliente"],
                id_empleado=empleado,
                fecha_entrega=datos["fecha_entrega"],
                estado=datos["estado"],
                total=total,
                observaciones=datos["observaciones"],
            )

            for i, p_data in enumerate(datos["prendas"]):
                prenda = Prenda.objects.create(
                    id_pedido=pedido,
                    tipo_prenda=p_data["tipo"],
                    color=p_data["color"],
                    peso=Decimal(str(p_data["peso"])),
                    cantidad=p_data["cantidad"],
                )
                DetalleServicio.objects.create(
                    id_prenda=prenda,
                    id_servicio=svc[p_data["servicio"]],
                    subtotal=Decimal(str(p_data["subtotal"])),
                )

            for estado in estados_historial[datos["estado"]]:
                EstadoPedido.objects.create(id_pedido=pedido, estado=estado)

            if datos["pago"]:
                Pago.objects.create(
                    id_pedido=pedido,
                    monto=datos["pago"]["monto"],
                    metodo_pago=datos["pago"]["metodo"],
                    estado_pago=datos["pago"]["estado"],
                )

        self.stdout.write("  Pedidos, prendas, servicios y pagos listos.")
