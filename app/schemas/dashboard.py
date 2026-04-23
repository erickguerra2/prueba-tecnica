"""Schemas Pydantic para los KPIs del Dashboard."""
from pydantic import BaseModel
from typing import List


class TotalesKPI(BaseModel):
    total_polizas: int
    total_items: int
    suma_valor_cif_usd: float
    suma_valor_dai: float


class TopItemOut(BaseModel):
    nombre: str
    total_valor_cif_usd: float


class ValorPorMesOut(BaseModel):
    mes: int
    total_valor_cif_usd: float
