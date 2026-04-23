# API Comercio Exterior

API RESTful para consulta y gestión de datos de Comercio Exterior de Guatemala. Incluye autenticación JWT, CRUD de pólizas con transacciones atómicas, y KPIs para dashboard analítico con caching.

## Características

- **Autenticación JWT**: Sistema de login seguro
- **CRUD de Pólizas**: Crear, leer, actualizar y eliminar pólizas con ítems en transacciones atómicas
- **Dashboard KPIs**: Endpoints con métricas cacheadas (totales, top ítems, valores por mes)
- **Dimensiones**: Consulta de datos maestros (aduanas, países, SAC, etc.)
- **Documentación**: API docs automática en `/docs` y `/redoc`

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **SQLite**: Base de datos ligera
- **Pydantic**: Validación de datos
- **JWT**: Autenticación segura
- **Cachetools**: Caching en memoria
- **Docker**: Containerización

## Instalación y Setup

### Prerrequisitos

- Python 3.13+
- uv (gestor de paquetes)

### Instalación

1. **Instalar uv** (si no lo tienes):
   ```bash
   pip install uv
   ```

2. **Crear entorno virtual e instalar dependencias**:
   ```bash
   uv venv
   uv pip sync
   ```

3. **Activar entorno**:
   - Windows: `.venv\Scripts\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`

4. **Configurar base de datos**:
   - Descomprimir `polizas_full.csv.zip` (si existe)
   - Ejecutar: `python setup.py`

### Ejecutar la API

```bash
uvicorn main:app --reload
```

La API estará disponible en: http://127.0.0.1:8000

Documentación: http://127.0.0.1:8000/docs

## Docker

### Construir y ejecutar con Docker Compose

```bash
docker-compose up --build
```

### Solo con Docker

```bash
docker build -t api-comercio-exterior .
docker run -p 8000:8000 -v $(pwd)/comercio_exterior.db:/app/comercio_exterior.db api-comercio-exterior
```

## Endpoints Principales

### Autenticación
- `POST /auth/login` - Login y obtener token JWT

### Pólizas (requiere auth)
- `POST /polizas` - Crear póliza con ítems (transacción atómica)
- `GET /polizas` - Listar pólizas (paginado)
- `GET /polizas/{id}` - Detalle de póliza con ítems
- `PUT /polizas/{id}` - Actualizar póliza con ítems (transacción atómica)
- `DELETE /polizas/{id}` - Eliminar póliza (transacción atómica)

### Dashboard KPIs (requiere auth, cacheado 5 min)
- `GET /dashboard/kpis` - KPIs generales
- `GET /dashboard/top-items` - Top 10 ítems por valor CIF
- `GET /dashboard/valor-por-mes` - Valor CIF agrupado por mes

### Dimensiones (requiere auth)
- `GET /dimensions/aduanas` - Lista de aduanas
- `GET /dimensions/paises` - Lista de países
- `GET /dimensions/sac` - Lista de códigos SAC
- `GET /dimensions/tipo-regimen` - Lista de tipos de régimen
- `GET /dimensions/tipo-unidad-medida` - Lista de unidades de medida

## Arquitectura

```
app/
├── api/           # Endpoints FastAPI
├── core/          # Configuración y seguridad
├── db/            # Modelos y conexión DB
├── schemas/       # Modelos Pydantic
└── services/      # Lógica de negocio (futuro)
```

## Base de Datos

- **SQLite**: `comercio_exterior.db`
- **Tablas principales**:
  - `polizas`: Cabeceras de pólizas
  - `poliza_items`: Ítems de pólizas
  - `users`: Usuarios para autenticación
  - Dimensiones: `aduanas`, `pais`, `sac`, `tipo_regimen`, `tipo_unidad_medida`

## Seguridad

- Autenticación JWT con expiración de 8 horas
- Passwords hasheados con bcrypt
- CORS configurado para desarrollo

## Caching

Los endpoints de dashboard usan cache en memoria con TTL de 5 minutos para mejorar performance.

## Testing

Para ejecutar tests (si existen):
```bash
pytest
```

## Despliegue

Para producción:
1. Cambiar `SECRET_KEY` en configuración
2. Usar variables de entorno para configuración sensible
3. Configurar base de datos PostgreSQL/MySQL si es necesario
4. Usar Redis para caching distribuido

## Licencia

Este proyecto es parte de una prueba técnica.