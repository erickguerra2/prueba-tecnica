"""
Modelos ORM de SQLAlchemy que mapean las tablas existentes de comercio_exterior.db
más la nueva tabla 'users' para autenticación.
"""
from datetime import date
from sqlalchemy import (
    Column, Integer, BigInteger, Float, String, Date,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.db.database import Base


# ──────────────────────────────────────────────
# Tablas de dimensión (ya existentes en la DB)
# ──────────────────────────────────────────────

class Aduana(Base):
    __tablename__ = "aduanas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    polizas = relationship("Poliza", back_populates="aduana")


class TipoRegimen(Base):
    __tablename__ = "tipo_regimen"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    polizas = relationship("Poliza", back_populates="tipo_regimen")


class Pais(Base):
    __tablename__ = "pais"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    items = relationship("PolizaItem", back_populates="pais")


class SAC(Base):
    __tablename__ = "sac"

    id = Column(Integer, primary_key=True, index=True)
    fraccion = Column(BigInteger, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)

    items = relationship("PolizaItem", back_populates="sac")


class TipoUnidadMedida(Base):
    __tablename__ = "tipo_unidad_medida"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    items = relationship("PolizaItem", back_populates="tipo_unidad_medida")


# ──────────────────────────────────────────────
# Tablas de hechos (ya existentes en la DB)
# ──────────────────────────────────────────────

class Poliza(Base):
    __tablename__ = "polizas"

    id = Column(Integer, primary_key=True, index=True)
    correlativo = Column(BigInteger, nullable=False, unique=True)
    fecha_declaracion = Column(Date, nullable=True)
    tipo_cambio_dolar = Column(Float, nullable=True)
    aduana_id = Column(Integer, ForeignKey("aduanas.id"), nullable=True)
    tipo_regimen_id = Column(Integer, ForeignKey("tipo_regimen.id"), nullable=True)

    aduana = relationship("Aduana", back_populates="polizas")
    tipo_regimen = relationship("TipoRegimen", back_populates="polizas")
    items = relationship("PolizaItem", back_populates="poliza", cascade="all, delete-orphan")


class PolizaItem(Base):
    __tablename__ = "poliza_items"

    id = Column(Integer, primary_key=True, index=True)
    poliza_id = Column(Integer, ForeignKey("polizas.id", ondelete="CASCADE"), nullable=True)
    sac_id = Column(Integer, ForeignKey("sac.id"), nullable=True)
    pais_id = Column(Integer, ForeignKey("pais.id"), nullable=True)
    tipo_unidad_medida_id = Column(Integer, ForeignKey("tipo_unidad_medida.id"), nullable=True)
    cantidad_fraccion = Column(Float, nullable=True)
    tasa_dai = Column(Float, nullable=True)
    valor_dai = Column(Float, nullable=True)
    valor_cif_uds = Column(Float, nullable=True)
    tasa_cif_cantidad_fraccion = Column(Float, nullable=True)

    poliza = relationship("Poliza", back_populates="items")
    sac = relationship("SAC", back_populates="items")
    pais = relationship("Pais", back_populates="items")
    tipo_unidad_medida = relationship("TipoUnidadMedida", back_populates="items")


# ──────────────────────────────────────────────
# Nueva tabla para autenticación
# ──────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
