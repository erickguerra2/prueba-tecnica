"""
Configuración central de la aplicación.
En producción, estos valores deben venir de variables de entorno o un archivo .env.
"""
from pydantic import BaseModel


class Settings(BaseModel):
    # Nombre de la app
    APP_NAME: str = "API Comercio Exterior"
    APP_VERSION: str = "1.0.0"

    # JWT
    SECRET_KEY: str = "cambiar-esto-en-produccion-por-una-clave-segura-aleatoria"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 horas

    # Base de datos
    DATABASE_URL: str = "sqlite:///./comercio_exterior.db"

    # Cache TTL en segundos (5 minutos)
    CACHE_TTL_SECONDS: int = 300


settings = Settings()
