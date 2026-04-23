"""
Script para crear las tablas nuevas (tabla 'users') en la base de datos existente.
Las tablas que ya existen NO son afectadas (checkfirst=True).
Ejecutar una sola vez: python create_tables.py
"""
from app.db.database import engine, Base
import app.db.models  # noqa: F401 - necesario para que SQLAlchemy registre los modelos

if __name__ == "__main__":
    print("Creando tablas nuevas en la base de datos...")
    Base.metadata.create_all(bind=engine, checkfirst=True)
    print("¡Listo! Tabla 'users' creada exitosamente.")
