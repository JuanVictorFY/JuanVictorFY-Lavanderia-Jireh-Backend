import requests

BASE_URL = "http://127.0.0.1:8001"
TOKEN    = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc5NzA1NzE3LCJpYXQiOjE3Nzk3MDIxMTcsImp0aSI6IjNlYjA3OWRjMWY2YjRmNGZhYTVhY2E4YWUwZDg5YzA5IiwidXNlcl9pZCI6MSwibm9tYnJlcyI6IkplYW4iLCJhcGVsbGlkb3MiOiJNZWppYSIsInJvbCI6ImFkbWluaXN0cmFkb3IiLCJlc3RhZG8iOnRydWV9.kuxYsSjlhVl5jHJk2sPqTk-7C-mBUrB4Wsl6Gh0VxbI"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type":  "application/json",
}

SERVICIOS = [
    {"nombre_servicio": "Lavado normal",      "descripcion": "Lavado estándar en frío por kilogramo",             "precio_base": "3.50"},
    {"nombre_servicio": "Lavado a vapor",     "descripcion": "Lavado profundo con vapor caliente por kilogramo",  "precio_base": "6.00"},
    {"nombre_servicio": "Lavado en seco",     "descripcion": "Para prendas delicadas sin uso de agua",            "precio_base": "9.00"},
    {"nombre_servicio": "Planchado",          "descripcion": "Solo planchado de prendas limpias",                 "precio_base": "4.00"},
    {"nombre_servicio": "Lavado + Planchado", "descripcion": "Combo lavado normal más planchado incluido",        "precio_base": "7.00"},
    {"nombre_servicio": "Desinfección",       "descripcion": "Lavado con desinfectante antibacterial especial",   "precio_base": "5.50"},
    {"nombre_servicio": "Lavado de edredón",  "descripcion": "Para edredones, mantas y cobertores gruesos",       "precio_base": "12.00"},
    {"nombre_servicio": "Lavado express",     "descripcion": "Entrega garantizada en 3 horas",                   "precio_base": "8.00"},
]

CLIENTES = [
    {"nombres": "María",  "apellidos": "García López",   "telefono": "987654321", "correo": "maria.garcia@gmail.com",  "direccion": "Av. Lima 123"},
    {"nombres": "Carlos", "apellidos": "Quispe Mamani",  "telefono": "976543210", "correo": "carlos.quispe@gmail.com", "direccion": "Jr. Cusco 456"},
    {"nombres": "Ana",    "apellidos": "Torres Flores",  "telefono": "965432109", "correo": "ana.torres@hotmail.com",  "direccion": "Calle Arequipa 789"},
    {"nombres": "Luis",   "apellidos": "Ramos Huanca",   "telefono": "954321098", "correo": "luis.ramos@gmail.com",    "direccion": "Av. Brasil 321"},
    {"nombres": "Rosa",   "apellidos": "Chávez Mendoza", "telefono": "943210987", "correo": "rosa.chavez@gmail.com",   "direccion": "Jr. Ayacucho 654"},
]

def seed(nombre, url, items, key):
    print(f"\n{'='*45}")
    print(f"  Creando {nombre}")
    print(f"{'='*45}")
    ok = 0
    for item in items:
        r = requests.post(f"{BASE_URL}{url}", json=item, headers=HEADERS)
        label = item.get(key, "")
        if r.status_code in [200, 201]:
            print(f"  ✅  {label} — ID: {r.json().get('id')}")
            ok += 1
        else:
            print(f"  ❌  {label} — Error {r.status_code}: {r.text[:100]}")
    print(f"\n  Resultado: {ok}/{len(items)} creados")

seed("SERVICIOS", "/api/servicios/", SERVICIOS, "nombre_servicio")
seed("CLIENTES",  "/api/clientes/",  CLIENTES,  "nombres")

print("\n✅  Seed completado exitosamente.")