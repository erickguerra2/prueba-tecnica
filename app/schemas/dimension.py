"""Schemas Pydantic para las tablas de dimensión (lookup)."""
from pydantic import BaseModel


class DimensionOut(BaseModel):
    """Schema genérico para cualquier tabla de dimensión (id + name)."""
    id: int
    name: str

    model_config = {"from_attributes": True}


class SACOut(BaseModel):
    """Schema para la tabla SAC (fracción arancelaria)."""
    id: int
    fraccion: int
    descripcion: str | None = None

    model_config = {"from_attributes": True}
