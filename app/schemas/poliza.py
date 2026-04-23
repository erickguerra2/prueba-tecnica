"""Schemas Pydantic para Pólizas e Items."""
from datetime import date
from typing import List, Optional
from pydantic import BaseModel


# ── Poliza Item ────────────────────────────────

class PolizaItemCreate(BaseModel):
    """Payload para crear un ítem de póliza."""
    sac_id: Optional[int] = None
    pais_id: Optional[int] = None
    tipo_unidad_medida_id: Optional[int] = None
    cantidad_fraccion: Optional[float] = None
    tasa_dai: Optional[float] = None
    valor_dai: Optional[float] = None
    valor_cif_uds: Optional[float] = None
    tasa_cif_cantidad_fraccion: Optional[float] = None


class PolizaItemOut(PolizaItemCreate):
    """Respuesta de un ítem de póliza."""
    id: int
    poliza_id: int

    model_config = {"from_attributes": True}


# ── Poliza ─────────────────────────────────────

class PolizaCreate(BaseModel):
    """Payload para crear una póliza con sus ítems (transacción atómica)."""
    correlativo: int
    fecha_declaracion: Optional[date] = None
    tipo_cambio_dolar: Optional[float] = None
    aduana_id: Optional[int] = None
    tipo_regimen_id: Optional[int] = None
    items: List[PolizaItemCreate] = []


class PolizaOut(BaseModel):
    """Respuesta de una póliza (cabecera sin ítems)."""
    id: int
    correlativo: int
    fecha_declaracion: Optional[date] = None
    tipo_cambio_dolar: Optional[float] = None
    aduana_id: Optional[int] = None
    tipo_regimen_id: Optional[int] = None

    model_config = {"from_attributes": True}


class PolizaDetailOut(PolizaOut):
    """Respuesta detallada de una póliza con sus ítems."""
    items: List[PolizaItemOut] = []


class PaginatedPolizas(BaseModel):
    """Respuesta paginada de pólizas."""
    total: int
    limit: int
    offset: int
    data: List[PolizaOut]
