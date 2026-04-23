"""
Punto de entrada de la API de Comercio Exterior.
Ejecutar con: uvicorn main:app --reload
Documentación en: http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, dimensions, polizas, dashboard

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "API RESTful para consulta y gestión de datos de Comercio Exterior de Guatemala. "
        "Incluye autenticación JWT, CRUD de pólizas y KPIs para dashboard analítico."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS (permite cualquier origen en desarrollo) ──────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(dimensions.router)
app.include_router(polizas.router)
app.include_router(dashboard.router)


# ── Health check ───────────────────────────────────────────────
@app.get("/", tags=["Health"], summary="Health check")
def root():
    """Verifica que la API está corriendo."""
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
