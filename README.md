# Lavanderia Jireh — Backend

API REST para el sistema de gestion de lavanderia. Gestiona pedidos, clientes, empleados, servicios, pagos y reportes, con autenticacion JWT y generacion de recibos PDF.

**API hosteada:** https://lavanderiajireh-api.onrender.com

## Tecnologias

- **Python 3.12** + **Django 5.2**
- **Django REST Framework 3.15**
- **SimpleJWT** — autenticacion con tokens de acceso y refresco
- **PostgreSQL** (Neon) — base de datos en produccion
- **psycopg 3** — driver PostgreSQL
- **ReportLab** — generacion de recibos PDF
- **openpyxl** — exportacion de reportes a Excel
- **qrcode** — QR en recibos
- **Gunicorn** + **Whitenoise** — servidor y archivos estaticos en produccion
- **Render** — plataforma de despliegue

## Requisitos

- Python 3.12+
- PostgreSQL o cadena de conexion a Neon

## Instalacion

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Variables de entorno

Crea un archivo `.env` basandote en `.env.example`:

```env
SECRET_KEY=tu-clave-secreta-larga-aqui
DATABASE_URL=postgresql://usuario:password@host/lavanderia_db?sslmode=require
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7
```

## Comandos

```bash
# Migraciones
python manage.py migrate

# Servidor de desarrollo
python manage.py runserver

# Crear superusuario admin
python manage.py createsuperuser

# Poblar base de datos con datos de prueba (requiere server activo)
python seed.py
```

## Estructura del proyecto

```
apps/
├── usuarios/     # Empleados, roles y autenticacion
├── clientes/     # Clientes y personas autorizadas
├── pedidos/      # Pedidos, prendas, estados y recibos PDF
├── servicios/    # Servicios disponibles y detalle por prenda
├── pagos/        # Registro de pagos
└── reportes/     # Estadisticas y exportacion Excel
config/
├── settings/
│   ├── base.py
│   ├── development.py
│   └── production.py
└── urls.py
core/
├── models.py      # Modelo base con timestamps
├── permissions.py # Permisos personalizados por rol
├── exceptions.py
└── pagination.py
```

## Roles del sistema

| Rol | Permisos |
|-----|----------|
| `administrador` | Acceso completo: empleados, reportes, configuracion |
| `recepcionista` | Pedidos, clientes, servicios, pagos |
| `operario` | Solo lectura de pedidos asignados |

## Endpoints principales

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | `/api/auth/login/` | Iniciar sesion |
| POST | `/api/auth/refresh/` | Refrescar token |
| GET/POST | `/api/pedidos/` | Listar / crear pedidos |
| POST | `/api/pedidos/{id}/cambiar-estado/` | Actualizar estado |
| GET | `/api/pedidos/{id}/recibo/` | Descargar recibo PDF |
| GET/POST | `/api/clientes/` | Clientes |
| GET/POST | `/api/servicios/` | Servicios |
| POST | `/api/servicios/detalles/calcular/` | Calcular precio por prenda |
| GET/POST | `/api/pagos/` | Pagos |
| GET | `/api/reportes/resumen/` | Resumen de estadisticas |
| GET | `/api/reportes/exportar/` | Exportar a Excel |
| GET | `/pedido/{codigo}/` | Consulta publica sin token |

Ver coleccion completa en `LavanClean_API.postman_collection.json`.
