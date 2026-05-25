import requests

BASE_URL = "http://127.0.0.1:8001"

def login():
    r = requests.post(f"{BASE_URL}/api/auth/login/", json={
        "username": "admin",
        "password": "admin"
    })
    data = r.json()
    token = data["access"]
    print(f"✅ Login exitoso — {data['empleado']['nombres']} {data['empleado']['apellidos']} ({data['empleado']['rol']})")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def step(titulo):
    print(f"\n{'─'*50}")
    print(f"  {titulo}")
    print(f"{'─'*50}")


def simular_pedido():

    H = login()

    # PASO 1 — Cliente ya existe
    step("PASO 1 — Cargar cliente existente")
    id_cliente = 1
    r = requests.get(f"{BASE_URL}/api/clientes/{id_cliente}/", headers=H)
    cliente = r.json()
    print(f"  ✅ Cliente — ID: {id_cliente} | {cliente['nombres']} {cliente['apellidos']}")

    # PASO 2 — Agregar persona autorizada
    step("PASO 2 — Agregar persona autorizada")
    r = requests.post(f"{BASE_URL}/api/clientes/{id_cliente}/personas-autorizadas/", headers=H, json={
        "nombres":  "Jorge García López",
        "dni":      "71234567",
        "telefono": "956789012"
    })
    persona = r.json()
    print(f"  ✅ Persona autorizada — {persona['nombres']} | DNI: {persona['dni']}")

    # PASO 3 — Crear pedido con prendas
    step("PASO 3 — Registrar pedido con prendas")
    r = requests.post(f"{BASE_URL}/api/pedidos/", headers=H, json={
        "id_cliente":    id_cliente,
        "id_empleado":   1,
        "fecha_entrega": "2026-05-26T17:00:00Z",
        "observaciones": "Cliente frecuente, trato preferencial",
        "prendas": [
            {"tipo_prenda": "Blusa",    "color": "Blanco", "peso": "0.30", "cantidad": 2, "observaciones": "Delicada"},
            {"tipo_prenda": "Pantalón", "color": "Negro",  "peso": "0.80", "cantidad": 2, "observaciones": None},
            {"tipo_prenda": "Vestido",  "color": "Rojo",   "peso": "0.50", "cantidad": 1, "observaciones": "Largo"},
            {"tipo_prenda": "Sábanas",  "color": "Beige",  "peso": "2.00", "cantidad": 1, "observaciones": "Matrimonial"},
        ]
    })
    pedido = r.json()
    id_pedido = pedido["id"]
    codigo    = pedido["codigo"]
    print(f"  ✅ Pedido creado — ID: {id_pedido} | Código: {codigo} | Estado: {pedido['estado']}")
    print(f"  Prendas registradas:")
    for p in pedido["prendas"]:
        print(f"    → ID {p['id']} | {p['tipo_prenda']} ({p['color']}) — {p['peso']} kg x{p['cantidad']}")

    # PASO 4 — Asignar servicios
    step("PASO 4 — Asignar servicios a cada prenda")

    # Blusa    → Lavado en seco     (id=3, S/9.00/kg)
    # Pantalón → Lavado + Planchado (id=5, S/7.00/kg)
    # Vestido  → Lavado en seco     (id=3, S/9.00/kg)
    # Sábanas  → Lavado normal      (id=1, S/3.50/kg)

    asignaciones = [
        (pedido["prendas"][0]["id"], 3, "Blusa    → Lavado en seco"),
        (pedido["prendas"][1]["id"], 5, "Pantalón → Lavado + Planchado"),
        (pedido["prendas"][2]["id"], 3, "Vestido  → Lavado en seco"),
        (pedido["prendas"][3]["id"], 1, "Sábanas  → Lavado normal"),
    ]

    for id_prenda, id_servicio, descripcion in asignaciones:
        r = requests.post(f"{BASE_URL}/api/servicios/detalles/calcular/", headers=H, json={
            "id_prenda":   id_prenda,
            "id_servicio": id_servicio
        })
        detalle = r.json()
        print(f"  ✅ {descripcion} — Subtotal: S/ {detalle['subtotal']}")

    # PASO 5 — Calcular total
    step("PASO 5 — Calcular total del pedido")
    r = requests.post(f"{BASE_URL}/api/pedidos/{id_pedido}/calcular-total/", headers=H)
    total = r.json()["total"]
    print(f"  ✅ Total calculado: S/ {total}")

    # PASO 6 — pendiente → en_proceso
    step("PASO 6 — Cambiar estado: pendiente → en_proceso")
    r = requests.patch(f"{BASE_URL}/api/pedidos/{id_pedido}/cambiar-estado/", headers=H, json={
        "estado":      "en_proceso",
        "descripcion": "Prendas recibidas e ingresadas a lavado"
    })
    print(f"  ✅ Estado: {r.json()['estado']} — correo enviado a {cliente['correo']}")

    # PASO 7 — Registrar pago
    step("PASO 7 — Registrar pago")
    r = requests.post(f"{BASE_URL}/api/pagos/", headers=H, json={
        "id_pedido":   id_pedido,
        "monto":       total,
        "metodo_pago": "yape"
    })
    pago = r.json()
    print(f"  ✅ Pago — ID: {pago['id']} | S/ {pago['monto']} | {pago['metodo_pago'].upper()} | {pago['estado_pago']}")

    # PASO 8 — en_proceso → listo
    step("PASO 8 — Cambiar estado: en_proceso → listo")
    r = requests.patch(f"{BASE_URL}/api/pedidos/{id_pedido}/cambiar-estado/", headers=H, json={
        "estado":      "listo",
        "descripcion": "Prendas lavadas y listas para recojo"
    })
    print(f"  ✅ Estado: {r.json()['estado']} — correo enviado a {cliente['correo']}")

    # PASO 9 — listo → entregado
    step("PASO 9 — Cambiar estado: listo → entregado")
    r = requests.patch(f"{BASE_URL}/api/pedidos/{id_pedido}/cambiar-estado/", headers=H, json={
        "estado":      "entregado",
        "descripcion": "Entregado a Jorge García López (persona autorizada)"
    })
    print(f"  ✅ Estado: {r.json()['estado']} — correo enviado a {cliente['correo']}")

    # PASO 10 — Consulta pública por código (sin token)
    step("PASO 10 — Consulta pública por código (sin token)")
    r = requests.get(f"{BASE_URL}/pedido/{codigo}/")
    data = r.json()
    print(f"  ✅ URL pública: {BASE_URL}/pedido/{codigo}/")
    print(f"  Cliente: {data['cliente']} | Estado: {data['estado_actual']} | Total: S/ {data['total']}")
    print(f"  Historial:")
    for h in data["historial"]:
        print(f"    → {h['estado']} | {h['descripcion']}")

    # PASO 11 — Historial del cliente
    step("PASO 11 — Historial completo del cliente")
    r = requests.get(f"{BASE_URL}/api/clientes/{id_cliente}/historial/", headers=H)
    historial = r.json()
    print(f"  ✅ {historial['cliente']['nombres']} {historial['cliente']['apellidos']}")
    print(f"  Total pedidos: {len(historial['pedidos'])}")
    for ped in historial["pedidos"]:
        print(f"    → Pedido #{ped['id']} [{ped.get('codigo','?')}] | {ped['estado']} | S/ {ped['total']}")

    print(f"\n{'='*50}")
    print(f"  ✅ SIMULACIÓN COMPLETADA")
    print(f"  Cliente : María García López")
    print(f"  Pedido  : #{id_pedido} | Código: {codigo}")
    print(f"  Total   : S/ {total} | YAPE")
    print(f"  Correos : 3 enviados a {cliente['correo']}")
    print(f"{'='*50}\n")


simular_pedido()