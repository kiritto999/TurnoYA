# TurnoYa API — FastAPI + MySQL + arquitectura multicapa

API REST para el proyecto TurnoYa. Está organizada por capas: controllers (HTTP), services (reglas de negocio), repositories (acceso a datos), models (SQLAlchemy), schemas (Pydantic) y core (configuración, BD y seguridad).

## 1. Base de datos

Ejecuta el archivo `turnoya_schema.sql` en MySQL. El esquema crea `turnoya_db`.

La API está configurada para MySQL local **sin contraseña** para el usuario `root`:

`mysql+pymysql://root:@localhost:3306/turnoya_db`

Si tu usuario MySQL no es `root`, cambia `DB_USER` en `.env`.

## 2. Instalación

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env # Linux/macOS
uvicorn app.main:app --reload
```

Swagger: http://127.0.0.1:8000/docs

## 3. Autenticación

El login devuelve JWT. Envía:

`Authorization: Bearer <token>`

La contraseña del usuario de TurnoYa **sí se almacena hasheada** (Argon2). Esto es independiente de la contraseña del servidor MySQL, que en tu caso está vacía.

## 4. Roles

- `cliente`
- `dueño`
- `empleado`
- `superadmin`

## 5. Endpoints principales

### Auth / RF01
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

### Negocios / RF02, RF11, RF14
- `POST /api/v1/businesses`
- `GET /api/v1/businesses`
- `GET /api/v1/businesses/{id}`
- `PUT /api/v1/businesses/{id}`
- `PATCH /api/v1/businesses/{id}/status`

### Sectores / RF03
- `POST /api/v1/businesses/{id}/sectors`
- `GET /api/v1/businesses/{id}/sectors`
- `GET /api/v1/sectors/{id}`
- `PUT /api/v1/sectors/{id}`
- `DELETE /api/v1/sectors/{id}`

### Catálogo / RF04
- `POST /api/v1/businesses/{id}/catalog`
- `GET /api/v1/businesses/{id}/catalog`
- `GET /api/v1/catalog/{id}`
- `PUT /api/v1/catalog/{id}`
- `DELETE /api/v1/catalog/{id}`

### Empleados / RF07, RF08
- `POST /api/v1/businesses/{id}/employees/invitations`
- `GET /api/v1/businesses/{id}/employees`
- `POST /api/v1/employee-invitations/{id}/accept`
- `PATCH /api/v1/employees/{id}/permissions`

### QR / RF05, RF06
- `POST /api/v1/businesses/{id}/qr`
- `GET /api/v1/businesses/{id}/qr`
- `GET /api/v1/qr/{code}`
- `GET /api/v1/qr/{code}/image`

### Turnos / RF09, RF10
- `POST /api/v1/businesses/{id}/turns`
- `GET /api/v1/businesses/{id}/queue`
- `GET /api/v1/turns/my`
- `GET /api/v1/turns/{id}`
- `PATCH /api/v1/turns/{id}/status`

### Notificaciones / RF12, RF13
- `GET /api/v1/notifications`
- `PATCH /api/v1/notifications/{id}/read`

## 6. Lo que queda preparado para ampliar

- Mapa: el esquema entregado no tiene latitud/longitud; por eso se implementa búsqueda por nombre/categoría, pero el endpoint de geolocalización deberá agregarse cuando se añadan esos campos.
- Push: el esquema guarda notificaciones. Para push real hay que conectar FCM, OneSignal, APNs u otro proveedor.

## 7. Prueba rápida

Registra un dueño, crea su negocio y luego usa Swagger para probar sectores, catálogo, QR y turnos.

## 8. Crear el superadministrador

Como RF14 es una función administrativa, no se habilita desde el registro público. Después de instalar dependencias:

```bash
python scripts/create_superadmin.py
```

## 9. Límites respecto al esquema original

RF02 menciona ubicación, y la idea menciona mapa; el esquema SQL entregado no contiene dirección, latitud ni longitud. La API no inventa esos datos. `optional_schema_extensions.sql` deja preparada una extensión para agregarlos.

RF12/RF13 describen alertas push/mensaje, pero el esquema original solo almacena notificaciones. La API crea y consulta esas notificaciones en MySQL; para push real hace falta integrar un proveedor y almacenar tokens de dispositivo.
