"""
Script de poblacion inicial — Lavanderia Jireh
Ejecutar con: python seed.py
"""
import sys, io, requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = "http://localhost:8000"


def login():
    r = requests.post(f"{BASE}/api/auth/login/", json={"username": "admin", "password": "admin123"})
    data = r.json()
    emp = data["empleado"]
    print(f"[OK] Login - {emp['nombres']} ({emp['rol']})")
    return {"Authorization": f"Bearer {data['access']}", "Content-Type": "application/json"}, emp["id"]


def get_all(H, url):
    r = requests.get(f"{BASE}{url}", headers=H)
    return r.json().get("results", [])


def post(H, url, body):
    r = requests.post(f"{BASE}{url}", headers=H, json=body)
    if r.status_code not in (200, 201):
        print(f"  [ERROR] {url} -> {r.status_code}: {r.text[:120]}")
        return None
    return r.json()


def patch(H, url, body):
    r = requests.patch(f"{BASE}{url}", headers=H, json=body)
    if r.status_code not in (200, 201):
        print(f"  [ERROR] PATCH {url} -> {r.status_code}: {r.text[:120]}")
    return r.json()


def upsert_servicio(H, data):
    existing = get_all(H, "/api/servicios/")
    match = next((s for s in existing if s["nombre_servicio"] == data["nombre_servicio"]), None)
    if match:
        return match
    return post(H, "/api/servicios/", data)


def upsert_cliente(H, data):
    existing = get_all(H, "/api/clientes/")
    match = next((c for c in existing if c["correo"] == data.get("correo") and data.get("correo")), None)
    if not match:
        match = next((c for c in existing
                      if c["nombres"] == data["nombres"] and c["apellidos"] == data["apellidos"]), None)
    if match:
        return match
    return post(H, "/api/clientes/", data)


def section(titulo):
    print(f"\n{'='*55}")
    print(f"  {titulo}")
    print(f"{'='*55}")


# ──────────────────────────────────────────────────────────────
H, id_empleado = login()

# ──────────────────────────────────────────────────────────────
section("SERVICIOS")
SERVICIOS = [
    {"nombre_servicio": "Lavado normal",     "descripcion": "Lavado estandar en frio por kg",            "precio_base": "3.50"},
    {"nombre_servicio": "Lavado a vapor",    "descripcion": "Lavado profundo con vapor caliente por kg", "precio_base": "6.00"},
    {"nombre_servicio": "Lavado en seco",    "descripcion": "Para prendas delicadas sin agua",           "precio_base": "9.00"},
    {"nombre_servicio": "Planchado",         "descripcion": "Solo planchado de prendas limpias",         "precio_base": "4.00"},
    {"nombre_servicio": "Lavado+Planchado",  "descripcion": "Combo lavado normal mas planchado",         "precio_base": "7.00"},
    {"nombre_servicio": "Desinfeccion",      "descripcion": "Lavado con desinfectante antibacterial",    "precio_base": "5.50"},
    {"nombre_servicio": "Lavado de edredon", "descripcion": "Para edredones y cobertores gruesos",       "precio_base": "12.00"},
    {"nombre_servicio": "Lavado express",    "descripcion": "Entrega garantizada en 3 horas",            "precio_base": "8.00"},
]

ids_servicios = []
for s in SERVICIOS:
    data = upsert_servicio(H, s)
    if data:
        ids_servicios.append(data["id"])
        print(f"  [+] {data['nombre_servicio']} - S/{data['precio_base']}/kg  (ID {data['id']})")

# ──────────────────────────────────────────────────────────────
section("CLIENTES")
CLIENTES = [
    {"nombres": "Maria",  "apellidos": "Garcia Lopez",    "telefono": "987654321", "correo": "maria.garcia@gmail.com",   "direccion": "Av. Lima 123"},
    {"nombres": "Carlos", "apellidos": "Quispe Mamani",   "telefono": "976543210", "correo": "carlos.quispe@gmail.com",  "direccion": "Jr. Cusco 456"},
    {"nombres": "Ana",    "apellidos": "Torres Flores",   "telefono": "965432109", "correo": "ana.torres@hotmail.com",   "direccion": "Calle Arequipa 789"},
    {"nombres": "Luis",   "apellidos": "Ramos Huanca",    "telefono": "954321098", "correo": "luis.ramos@gmail.com",     "direccion": "Av. Brasil 321"},
    {"nombres": "Rosa",   "apellidos": "Chavez Mendoza",  "telefono": "943210987", "correo": "rosa.chavez@gmail.com",    "direccion": "Jr. Ayacucho 654"},
    {"nombres": "Pedro",  "apellidos": "Vargas Salinas",  "telefono": "932109876", "correo": "pedro.vargas@outlook.com", "direccion": "Av. Colonial 987"},
    {"nombres": "Lucia",  "apellidos": "Morales Paredes", "telefono": "921098765", "correo": "lucia.morales@gmail.com",  "direccion": "Calle San Martin 12"},
    {"nombres": "Jorge",  "apellidos": "Huanca Ticona",   "telefono": "910987654", "correo": None,                       "direccion": "Jr. Independencia 45"},
]

ids_clientes = []
for c in CLIENTES:
    data = upsert_cliente(H, c)
    if data:
        ids_clientes.append(data["id"])
        print(f"  [+] {data['nombres']} {data['apellidos']}  (ID {data['id']})")

if len(ids_clientes) < 8:
    print(f"  [!] Solo se obtuvieron {len(ids_clientes)} clientes, ajustando pedidos...")
    while len(ids_clientes) < 8:
        ids_clientes.append(ids_clientes[0])

# ──────────────────────────────────────────────────────────────
section("PEDIDOS")

PEDIDOS_SPEC = [
    # Entregados con pago
    {
        "id_cliente": ids_clientes[0],
        "prendas": [
            {"tipo_prenda": "Blusa",    "color": "Blanco", "peso": "0.30", "cantidad": 2, "observaciones": "Delicada"},
            {"tipo_prenda": "Pantalon", "color": "Negro",  "peso": "0.80", "cantidad": 2, "observaciones": ""},
            {"tipo_prenda": "Vestido",  "color": "Rojo",   "peso": "0.50", "cantidad": 1, "observaciones": "Largo"},
        ],
        "estados": ["en_proceso", "listo", "entregado"],
        "metodo_pago": "yape",
        "servicios": [2, 4, 2],
    },
    {
        "id_cliente": ids_clientes[1],
        "prendas": [
            {"tipo_prenda": "Camisa",  "color": "Azul",  "peso": "0.40", "cantidad": 3, "observaciones": ""},
            {"tipo_prenda": "Sabanas", "color": "Beige", "peso": "2.00", "cantidad": 2, "observaciones": "Matrimonial"},
        ],
        "estados": ["en_proceso", "listo", "entregado"],
        "metodo_pago": "efectivo",
        "servicios": [4, 0],
    },
    {
        "id_cliente": ids_clientes[2],
        "prendas": [
            {"tipo_prenda": "Edredon",  "color": "Gris",   "peso": "3.50", "cantidad": 1, "observaciones": "Doble"},
            {"tipo_prenda": "Almohada", "color": "Blanco", "peso": "0.60", "cantidad": 2, "observaciones": ""},
        ],
        "estados": ["en_proceso", "listo", "entregado"],
        "metodo_pago": "plin",
        "servicios": [6, 0],
    },
    # Listos para recoger
    {
        "id_cliente": ids_clientes[3],
        "prendas": [
            {"tipo_prenda": "Terno",  "color": "Negro",  "peso": "1.20", "cantidad": 1, "observaciones": "Importante"},
            {"tipo_prenda": "Camisa", "color": "Blanco", "peso": "0.35", "cantidad": 2, "observaciones": ""},
        ],
        "estados": ["en_proceso", "listo"],
        "metodo_pago": "tarjeta",
        "servicios": [2, 3],
    },
    {
        "id_cliente": ids_clientes[4],
        "prendas": [
            {"tipo_prenda": "Vestido", "color": "Verde", "peso": "0.60", "cantidad": 1, "observaciones": ""},
            {"tipo_prenda": "Blusa",   "color": "Rosa",  "peso": "0.25", "cantidad": 2, "observaciones": ""},
        ],
        "estados": ["en_proceso", "listo"],
        "metodo_pago": None,
        "servicios": [4, 1],
    },
    # En proceso
    {
        "id_cliente": ids_clientes[5],
        "prendas": [
            {"tipo_prenda": "Jeans", "color": "Azul",   "peso": "0.90", "cantidad": 3, "observaciones": ""},
            {"tipo_prenda": "Polo",  "color": "Blanco", "peso": "0.20", "cantidad": 5, "observaciones": ""},
        ],
        "estados": ["en_proceso"],
        "metodo_pago": None,
        "servicios": [0, 0],
    },
    {
        "id_cliente": ids_clientes[6],
        "prendas": [
            {"tipo_prenda": "Cortinas", "color": "Crema", "peso": "2.80", "cantidad": 2, "observaciones": "Pesadas"},
        ],
        "estados": ["en_proceso"],
        "metodo_pago": None,
        "servicios": [7],
    },
    # Pendientes
    {
        "id_cliente": ids_clientes[7],
        "prendas": [
            {"tipo_prenda": "Camisa",   "color": "Celeste", "peso": "0.35", "cantidad": 4, "observaciones": ""},
            {"tipo_prenda": "Pantalon", "color": "Gris",    "peso": "0.75", "cantidad": 2, "observaciones": ""},
        ],
        "estados": [],
        "metodo_pago": None,
        "servicios": [3, 3],
    },
    {
        "id_cliente": ids_clientes[0],
        "prendas": [
            {"tipo_prenda": "Abrigo", "color": "Marron", "peso": "1.50", "cantidad": 1, "observaciones": "Cuidado especial"},
        ],
        "estados": [],
        "metodo_pago": None,
        "servicios": [2],
    },
    # Cancelado
    {
        "id_cliente": ids_clientes[2],
        "prendas": [
            {"tipo_prenda": "Chompa", "color": "Azul", "peso": "0.60", "cantidad": 2, "observaciones": ""},
        ],
        "estados": ["cancelado"],
        "metodo_pago": None,
        "servicios": [0],
    },
]

MENSAJES = {
    "en_proceso": "Prendas ingresadas a lavado",
    "listo":      "Prendas listas para recojo",
    "entregado":  "Pedido entregado al cliente",
    "cancelado":  "Cliente cancelo el pedido",
}

for i, spec in enumerate(PEDIDOS_SPEC, 1):
    pedido = post(H, "/api/pedidos/", {
        "id_cliente":    spec["id_cliente"],
        "id_empleado":   id_empleado,
        "prendas":       spec["prendas"],
        "fecha_entrega": "2026-06-01T16:00:00Z",
    })
    if not pedido:
        continue

    pid    = pedido["id"]
    codigo = pedido["codigo"]

    for j, prenda in enumerate(pedido["prendas"]):
        if j < len(spec["servicios"]) and spec["servicios"][j] < len(ids_servicios):
            post(H, "/api/servicios/detalles/calcular/", {
                "id_prenda":   prenda["id"],
                "id_servicio": ids_servicios[spec["servicios"][j]],
            })

    total_res = post(H, f"/api/pedidos/{pid}/calcular-total/", {})
    total = total_res["total"] if total_res else "0.00"

    for estado in spec["estados"]:
        patch(H, f"/api/pedidos/{pid}/cambiar-estado/", {
            "estado":      estado,
            "descripcion": MENSAJES.get(estado, ""),
        })

    if spec["metodo_pago"]:
        post(H, "/api/pagos/", {
            "id_pedido":   pid,
            "monto":       total,
            "metodo_pago": spec["metodo_pago"],
        })

    estado_final = spec["estados"][-1] if spec["estados"] else "pendiente"
    pago_str = f"| Pago: {spec['metodo_pago'].upper()}" if spec["metodo_pago"] else ""
    print(f"  [+] Pedido {i:02d} [{codigo}] - {estado_final:10s} | S/{total} {pago_str}")

# ──────────────────────────────────────────────────────────────
section("RESUMEN FINAL")
r  = requests.get(f"{BASE}/api/pedidos/",    headers=H)
r2 = requests.get(f"{BASE}/api/clientes/",  headers=H)
r3 = requests.get(f"{BASE}/api/servicios/", headers=H)
r4 = requests.get(f"{BASE}/api/pagos/",     headers=H)

print(f"  Servicios : {r3.json().get('count', '?')}")
print(f"  Clientes  : {r2.json().get('count', '?')}")
print(f"  Pedidos   : {r.json().get('count',  '?')}")
print(f"  Pagos     : {r4.json().get('count',  '?')}")
print(f"\n  Listo! Base de datos poblada correctamente.")
