# MANUAL TÉCNICO

# Sistema ICTIOLÓGICO – Monitoreo de Fauna Acuática

## 1. Introducción

El Sistema ICTIOLÓGICO es una plataforma compuesta por una aplicación móvil desarrollada en Flutter y una API REST desarrollada en FastAPI, diseñada para apoyar la recolección, almacenamiento y sincronización de información biológica obtenida durante eventos de muestreo ictiológico.

El sistema implementa una estrategia Offline First, permitiendo registrar información en campo sin conexión a internet mediante una base de datos SQLite local y sincronizar posteriormente los registros con PostgreSQL cuando exista conectividad.

---

# 2. Arquitectura General

```text
Flutter Mobile App
        │
        ▼
SQLite Local Database
        │
        ▼
SyncService
        │
        ▼
FastAPI REST API
        │
        ▼
PostgreSQL
```

---

# 3. Arquitectura Backend

## Framework

* FastAPI

## Patrón de diseño

Repository Pattern

## Estructura

```text
backend_app_ictiologica/

app/
├── api/
├── models/
├── repositories/
├── schemas/
├── services/
├── utils/

storage/
├── evidencias/
└── salida_evidencias/

Scripts_db/
└── db_tesis.sql
```

---

# 4. Tecnologías Backend

| Tecnología        | Versión |
| ----------------- | ------- |
| Python            | 3.13    |
| FastAPI           | 0.136.1 |
| SQLAlchemy        | 2.0.49  |
| PostgreSQL        | 17.x    |
| Uvicorn           | 0.46.0  |
| Pydantic          | 2.13.4  |
| JWT (python-jose) | 3.5.0   |
| Passlib           | 1.7.4   |
| BCrypt            | 4.0.1   |
| psycopg2-binary   | 2.9.12  |
| python-dotenv     | 1.2.2   |

---

# 5. Dependencias Backend

```bash
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
pydantic-settings
python-dotenv
python-jose
passlib
bcrypt
python-multipart
email-validator
```

Instalación:

```bash
pip install -r requirements.txt
```

---

# 6. Arquitectura Frontend

## Framework

Flutter

## Gestión de Estado

Provider

## Patrón utilizado

Presentation
↓
Provider
↓
Repository
↓
Datasource
↓
API / SQLite

## Estructura

```text
frontend_app_ictiologica/

lib/
├── app/
├── core/
├── features/
├── shared/
└── main.dart
```

---

# 7. Tecnologías Frontend

| Tecnología             | Versión |
| ---------------------- | ------- |
| Flutter                | 3.41.9  |
| Dart                   | 3.11.5  |
| Provider               | 6.1.5+1 |
| Dio                    | 5.9.2   |
| SQLite (sqflite)       | 2.4.2   |
| Geolocator             | 13.0.4  |
| Connectivity Plus      | 6.1.5   |
| Image Picker           | 1.2.1   |
| Flutter Secure Storage | 9.2.4   |
| Path Provider          | 2.1.5   |
| UUID                   | 4.5.3   |
| Intl                   | 0.20.2  |

---

# 8. Dependencias Frontend

```bash
provider
dio
sqflite
path
path_provider
connectivity_plus
geolocator
image_picker
flutter_secure_storage
uuid
intl
```

Instalación:

```bash
flutter pub get
```

---

# 9. Modelo de Datos

## Usuario

Gestiona autenticación y permisos.

Campos principales:

* usuario_id
* nombre
* correo
* contrasena
* institucion
* rol_id

---

## Salida

Representa un evento de muestreo.

Campos principales:

* salida_id
* nombre_lugar
* nombre_proyecto
* fecha_inicio
* fecha_fin
* observaciones
* estado

Estados:

* abierta
* cerrada

---

## Ocurrencia

Representa un individuo observado o capturado.

Campos principales:

* id_ocurrencia
* id_especie
* salida_id
* fecha_hora
* latitud
* longitud
* altitud
* longitud_pez
* peso
* sexo
* estacion_id

---

## Estación

Representa un punto oficial de monitoreo.

Campos:

* estacion_id
* codigo
* nombre
* cuerpo_agua
* latitud
* longitud
* activo

---

## Medición

Variables fisicoquímicas asociadas a una ocurrencia.

Ejemplos:

* oxigeno_disuelto_mg_l
* ph
* conductividad_us_cm
* temperatura_c
* nitratos_mg_l
* fosfatos_mg_l
* salinidad

---

## Evidencia

Archivos multimedia asociados a ocurrencias.

Campos:

* id_foto
* id_ocurrencia
* ruta
* observaciones

---

# 10. Georreferenciación

El sistema obtiene automáticamente:

* Latitud
* Longitud
* Altitud

mediante GPS del dispositivo.

Posteriormente el backend identifica la estación más cercana utilizando la fórmula de Haversine.

Flujo:

```text
GPS
 ↓
Latitud / Longitud
 ↓
find_nearest_estacion()
 ↓
estacion_id
```

Las estaciones son administradas exclusivamente por el sistema.

El usuario no puede:

* Crear estaciones
* Editar estaciones
* Eliminar estaciones

---

# 11. Persistencia Local

Base de datos:

```text
ictiologia_app.db
```

Tablas:

* species
* salidas
* ocurrencias
* mediciones
* evidencias
* salida_evidencia

---

# 12. Estrategia Offline

Cada registro local posee:

```text
sync_status
is_deleted
updated_at_local
```

Estados:

```text
pending
synced
```

---

# 13. Servicio de Sincronización

Componente:

```text
SyncService
```

Orden de sincronización:

```text
1. Salidas
2. Ocurrencias
3. Mediciones
4. Evidencias
```

Este orden garantiza la integridad referencial.

---

# 14. Seguridad

Autenticación mediante JWT.

Formato:

```http
Authorization: Bearer <token>
```

Los tokens se almacenan localmente mediante:

```text
Flutter Secure Storage
```

---

# 15. Evidencias

Las evidencias se almacenan utilizando el formato:

```text
CODIGO_OCURRENCIA_FAAAAMMDD_HHMMSS.ext
```

Ejemplo:

```text
OCC001_F20260618_H141530.jpg
```

Donde:

* F = Fecha
* H = Hora

---

# 16. Flujo Funcional del Sistema

```text
Usuario
 ↓
Crear salida
 ↓
Registrar ocurrencia
 ↓
Capturar GPS
 ↓
Asignar estación automáticamente
 ↓
Registrar medición
 ↓
Adjuntar evidencia
 ↓
Sincronizar
 ↓
PostgreSQL
```

---

# 17. Instalación en Windows

## Requisitos

* Git
* Python 3.12+
* PostgreSQL 15+
* Flutter 3.24+
* Android Studio

## Clonar Backend

```bash
git clone <URL_BACKEND>
cd backend_app_ictiologica
```

## Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Crear archivo .env

```env
DATABASE_URL=postgresql://postgres:123456@localhost:5432/ictiologia
SECRET_KEY=clave_secreta
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Crear Base de Datos

```sql
CREATE DATABASE ictiologia;
```

## Ejecutar Script

```text
Scripts_db/db_tesis.sql
```

## Crear Rol Inicial

```sql
INSERT INTO roles (
    nombre_rol,
    descripcion
)
VALUES (
    'Investigador',
    'Se puede dejar null'
);
```

## Ejecutar Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# 18. Instalación Frontend

## Clonar

```bash
git clone <URL_FRONTEND>
cd frontend_app_ictiologica
```

## Instalar dependencias

```bash
flutter pub get
```

---

# 19. Configuración de IP

Cuando se despliegue el proyecto en otro computador debe actualizarse la IP del backend en los siguientes archivos:

```text
lib/app/core/network/api_client.dart

lib/features/evidencias/presentation/pages/evidencia_create_page.dart

lib/features/evidencias/presentation/pages/detail_page.dart

lib/features/ocurrencias/presentation/pages/ocurrencia_create_page.dart
```

Ejemplo:

```dart
const String baseUrl =
"http://192.168.1.100:8000/api/v1";
```

Obtener IP local:

Windows:

```bash
ipconfig
```

macOS:

```bash
ifconfig
```

---

# 20. Ejecución Flutter

```bash
flutter run
```

---

# 21. Verificación Final

Backend:

```text
http://localhost:8000/docs
```

Frontend:

```bash
flutter run
```

Pruebas recomendadas:

1. Registrar usuario.
2. Iniciar sesión.
3. Crear salida.
4. Crear ocurrencia.
5. Obtener GPS.
6. Asociar estación.
7. Registrar medición.
8. Registrar evidencia.
9. Probar modo offline.
10. Ejecutar sincronización.

---

# 22. Licencia

Proyecto académico desarrollado como apoyo a procesos de monitoreo ictiológico y gestión de información biológica en estudios ambientales.
