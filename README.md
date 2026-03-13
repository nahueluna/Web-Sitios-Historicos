# Web Sitios Históricos

Plataforma web para subir, explorar y reseñar sitios históricos de Argentina. Permite a los usuarios descubrir lugares de interés histórico, dejar reseñas con calificaciones, marcar favoritos y explorar sitios a través de mapas interactivos.

Sistema desarrollado para la asignatura **Proyecto de Software** de la Licenciatura en Informática y Sistemas — Universidad Nacional de La Plata.

## Demo

- **Backend (API + Admin):** https://sitios-historicos-api.onrender.com/
- **Frontend (Portal):** Aun no disponible.

## Arquitectura

El sistema se divide en dos módulos independientes:

```
web-sitios-historicos/
├── admin/          # Backend — API REST + panel de administración
├── portal/         # Frontend — aplicación pública SPA
└── render.yaml     # Configuración de despliegue en Render
```

## Backend (`admin/`)

API REST y panel de administración construido con **Flask**. Expone endpoints públicos bajo el prefijo `/api/` consumidos por el portal, y un panel server-side para gestionar usuarios, sitios, reseñas, etiquetas y feature flags.

### Tecnologías

- **Flask 3.1** — Framework web
- **SQLAlchemy 2.x** (flask-sqlalchemy-lite) — ORM
- **PostgreSQL 16** — Base de datos relacional
- **GeoAlchemy2** — Consultas geográficas (búsqueda por radio)
- **Marshmallow 4.1** — Validación y serialización de datos
- **Flask-JWT-Extended** — Autenticación por tokens JWT (access + refresh)
- **Flask-Bcrypt** — Hashing de contraseñas
- **MinIO** — Almacenamiento de imágenes (S3-compatible)
- **Google Auth** — OAuth2 con Google
- **Gunicorn** — Servidor WSGI de producción
- **Poetry** — Gestión de dependencias

### Funcionalidades principales

- API REST con paginación, filtros y búsqueda geográfica por radio
- Autenticación por sesión (admin) y JWT (API pública)
- Login con Google OAuth2
- RBAC: roles Público, Editor, Admin y System Admin con permisos granulares
- Moderación de reseñas (pendiente → aprobada / rechazada)
- ABM de sitios, categorías, estados de conservación y etiquetas
- Feature flags: modo mantenimiento (admin/portal) y toggle de reseñas
- Almacenamiento de imágenes en MinIO/S3
- Exportación de sitios a CSV
- Logs de auditoría

## Frontend (`portal/`)

SPA pública construida con **Vue.js 3** que consume la API REST del backend.

### Tecnologías

- **Vue.js 3.5** (Composition API + `<script setup>`) — Framework reactivo
- **Vite 7.1** — Build tool
- **Pinia 3.0** — Estado global
- **Vue Router 4.5** — Enrutamiento SPA
- **Axios 1.13** — Cliente HTTP con interceptores para refresh de tokens
- **Bootstrap 5.3 + CoreUI Vue** — Componentes de UI
- **Leaflet 1.9** — Mapas interactivos con OpenStreetMap
- **vue3-google-login** — Login con Google OAuth2

### Funcionalidades principales

- Explorar sitios con filtros por nombre, ciudad, provincia y etiquetas
- Búsqueda geográfica por radio en mapa interactivo
- Detalle de sitio con galería de imágenes, mapa y reseñas
- Registro e inicio de sesión con Google
- Crear, editar y eliminar reseñas propias (una por sitio, rating 1-5)
- Gestionar sitios favoritos
- Perfil de usuario con historial de reseñas y favoritos
- Refresh automático de tokens JWT

## Requisitos previos

- **Python** >= 3.10
- **Node.js** >= 20.19.0 o >= 22.12.0
- **PostgreSQL** 16
- **MinIO** (desarrollo local) o servicio S3-compatible (producción)
- **Poetry** >= 2.1

## Instalación

### Backend

```bash
cd admin
cp .env.example .env          # Completar con los valores correspondientes
poetry install
poetry run flask --app "src.web:create_app('development')" run
```

### Frontend

```bash
cd portal
npm install
# Crear .env con VITE_API_URL y VITE_GOOGLE_CLIENT_ID
npm run dev
```
