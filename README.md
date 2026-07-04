# MANUAL TÉCNICO

# Sistema ICTIOLÓGICO 

> **Versión:** 1.0\
> **Arquitectura:** Flutter + FastAPI + PostgreSQL + SQLite (Offline
> First)

------------------------------------------------------------------------

# Tabla de Contenido

1.  Descripción General
2.  Arquitectura
3.  Requisitos Previos
4.  Instalación Backend (Windows y macOS)
5.  Instalación Frontend (Windows y macOS)
6.  Configuración de la Base de Datos
7.  Configuración del Proyecto
8.  Ejecución
9.  Arquitectura del Código
10. Modelo de Datos
11. Modo Offline
12. Sincronización
13. Manejo de Evidencias
14. Verificación
15. Solución de Problemas

------------------------------------------------------------------------

# 1. Descripción General

El Sistema ICTIOLÓGICO es una plataforma para el registro de información
obtenida durante campañas de muestreo ictiológico.

Está compuesto por:

-   Aplicación móvil desarrollada en Flutter.
-   API REST desarrollada en FastAPI.
-   Base de datos PostgreSQL.
-   Base de datos SQLite para funcionamiento Offline First.

Características principales:

-   Registro de salidas de campo.
-   Gestión de ocurrencias.
-   Registro de mediciones fisicoquímicas.
-   Captura de evidencias fotográficas.
-   Georreferenciación automática.
-   Sincronización entre SQLite y PostgreSQL.

------------------------------------------------------------------------

# 2. Arquitectura

``` text
Flutter
   │
SQLite (Offline)
   │
SyncService
   │
FastAPI
   │
PostgreSQL
```

------------------------------------------------------------------------

# 3. Requisitos Previos

## Herramientas necesarias

### Obligatorias

-   Git
-   Python 3.13 o superior
-   pip
-   Flutter SDK 3.41+
-   Dart SDK (incluido con Flutter)
-   Android Studio (SDK + Emulator)
-   PostgreSQL 17+
-   pgAdmin (opcional)
-   VS Code o Android Studio

### Verificar instalación

``` bash
python --version
python3 --version

flutter doctor

dart --version

psql --version

git --version
```

> En macOS normalmente se utiliza `python3`; en Windows puede utilizarse
> `python`.

------------------------------------------------------------------------

# 4. Instalación Backend

## Windows

``` bash
git clone <URL_BACKEND>
cd backend_app_ictiologica

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

## macOS

``` bash
git clone <URL_BACKEND>
cd backend_app_ictiologica

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Crear archivo `.env`

``` env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ictiologia
SECRET_KEY=CAMBIAR_CLAVE
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Ejecutar:

``` bash
uvicorn app.main:app --reload
```

Swagger:

    http://localhost:8000/docs

------------------------------------------------------------------------

# 5. Instalación Frontend

## Windows

``` bash
git clone <URL_FRONTEND>
cd frontend_app_ictiologica

flutter pub get

flutter run
```

## macOS

``` bash
git clone <URL_FRONTEND>
cd frontend_app_ictiologica

flutter pub get

flutter run
```

Verificar instalación:

``` bash
flutter doctor
```

------------------------------------------------------------------------

# 6. Configuración PostgreSQL

Crear base de datos:

``` sql
CREATE DATABASE ictiologia;
```

Ejecutar:

    Scripts_db/db_tesis.sql

Crear el rol inicial si aplica.

------------------------------------------------------------------------

# 7. Configuración del Proyecto

Actualizar la URL del backend cuando cambie la máquina.

Archivos principales:

``` text
lib/app/core/network/api_client.dart
lib/features/evidencias/presentation/pages/evidencia_create_page.dart
lib/features/evidencias/presentation/pages/detail_page.dart
lib/features/ocurrencias/presentation/pages/ocurrencia_create_page.dart
```

Ejemplo:

``` dart
const String baseUrl = "http://192.168.1.100:8000/api/v1";
```

Obtener IP:

Windows

``` bash
ipconfig
```

macOS

``` bash
ifconfig
```

------------------------------------------------------------------------

# 8. Arquitectura del Proyecto

## Backend

``` text
app/
├── api
├── models
├── repositories
├── schemas
├── services
├── utils
```

## Frontend

``` text
lib/
├── app
├── core
├── features
├── shared
└── main.dart
```

Patrón utilizado:

``` text
Presentation
    ↓
Provider
    ↓
Repository
    ↓
Datasource
    ↓
API / SQLite
```

------------------------------------------------------------------------

# 9. Tecnologías

## Backend

-   FastAPI
-   SQLAlchemy
-   PostgreSQL
-   Pydantic
-   JWT
-   Uvicorn

## Frontend

-   Flutter
-   Dart
-   Provider
-   Dio
-   SQLite (sqflite)
-   Connectivity Plus
-   Geolocator
-   Image Picker
-   Flutter Secure Storage
-   UUID

------------------------------------------------------------------------

# 10. Modelo de Datos

Entidades principales:

-   Usuario
-   Salida
-   Estación
-   Ocurrencia
-   Medición
-   Evidencia
-   Especie

------------------------------------------------------------------------

# 11. Offline First

Persistencia local:

    ictiologia_app.db

Tablas:

-   species
-   salidas
-   ocurrencias
-   mediciones
-   evidencias

Campos de sincronización:

    sync_status
    is_deleted
    updated_at_local

Estados:

-   pending_create
-   pending_update
-   pending_delete
-   synced

------------------------------------------------------------------------

# 12. Sincronización

Orden de sincronización:

1.  Salidas
2.  Ocurrencias
3.  Mediciones
4.  Evidencias

Este orden mantiene la integridad referencial.

------------------------------------------------------------------------

# 13. Evidencias

Durante el modo offline:

-   La imagen se almacena localmente.
-   Se sincroniza posteriormente con el servidor.
-   El backend almacena los archivos en:

```{=html}
<!-- -->
```
    storage/evidencias/

------------------------------------------------------------------------

# 14. Verificación

Backend:

    http://localhost:8000/docs

Frontend:

``` bash
flutter run
```

Pruebas recomendadas:

1.  Iniciar sesión.
2.  Crear salida.
3.  Registrar ocurrencia.
4.  Registrar medición.
5.  Registrar evidencia.
6.  Probar modo offline.
7.  Ejecutar sincronización.
8.  Validar registros en PostgreSQL.

------------------------------------------------------------------------

# 15. Solución de Problemas

## Flutter

``` bash
flutter clean
flutter pub get
flutter doctor
```

## Python

Windows

``` bash
venv\Scripts\activate
```

macOS

``` bash
source venv/bin/activate
```

## Base de datos

Verificar:

-   PostgreSQL iniciado.
-   Credenciales del `.env`.
-   Base de datos creada.
-   Script SQL ejecutado.

------------------------------------------------------------------------

**Proyecto desarrollado como apoyo al monitoreo ictiológico con
arquitectura Offline First.**
