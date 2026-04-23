"""
Configuración de la conexión a la base de datos SQLite usando SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# La base de datos ya fue creada por setup.py
DATABASE_URL = "sqlite:///./comercio_exterior.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Necesario para SQLite con FastAPI
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Clase base para todos los modelos ORM."""
    pass


def get_db():
    """
    Generador de sesiones de base de datos.
    Usado como dependencia de FastAPI (Dependency Injection).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
