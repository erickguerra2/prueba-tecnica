"""
Endpoints del Dashboard con KPIs y caching.
  GET /dashboard/kpis         - KPIs generales con cache
  GET /dashboard/top-items    - Top 10 ítems por valor CIF con cache
  GET /dashboard/valor-por-mes - Valor CIF por mes con cache

Todos los endpoints requieren autenticación JWT.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from cachetools import TTLCache, cached

from app.db.database import get_db
from app.db.models import Poliza, PolizaItem, SAC
from app.schemas.dashboard import TotalesKPI, TopItemOut, ValorPorMesOut
from app.core.security import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_user)],
)

# Cache con TTL de 5 minutos
cache = TTLCache(maxsize=100, ttl=300)


@router.get(
    "/kpis",
    response_model=TotalesKPI,
    summary="KPIs generales del dashboard",
)
@cached(cache)
def get_kpis(db: Session = Depends(get_db)):
    """
    Devuelve KPIs generales: total pólizas, total ítems, suma valor CIF USD, suma valor DAI.
    Resultados cacheados por 5 minutos.
    """
    total_polizas = db.query(Poliza).count()
    total_items = db.query(PolizaItem).count()
    suma_valor_cif = db.query(func.sum(PolizaItem.valor_cif_uds)).scalar() or 0.0
    suma_valor_dai = db.query(func.sum(PolizaItem.valor_dai)).scalar() or 0.0

    return TotalesKPI(
        total_polizas=total_polizas,
        total_items=total_items,
        suma_valor_cif_usd=suma_valor_cif,
        suma_valor_dai=suma_valor_dai,
    )


@router.get(
    "/top-items",
    response_model=list[TopItemOut],
    summary="Top 10 ítems por valor CIF",
)
@cached(cache)
def get_top_items(db: Session = Depends(get_db)):
    """
    Devuelve los top 10 ítems (por descripción SAC) ordenados por suma de valor CIF USD descendente.
    Resultados cacheados por 5 minutos.
    """
    results = (
        db.query(
            SAC.descripcion.label("nombre"),
            func.sum(PolizaItem.valor_cif_uds).label("total_valor_cif_usd"),
        )
        .join(PolizaItem, SAC.id == PolizaItem.sac_id)
        .group_by(SAC.descripcion)
        .order_by(func.sum(PolizaItem.valor_cif_uds).desc())
        .limit(10)
        .all()
    )

    return [
        TopItemOut(nombre=row.nombre or "Sin descripción", total_valor_cif_usd=row.total_valor_cif_usd or 0.0)
        for row in results
    ]


@router.get(
    "/valor-por-mes",
    response_model=list[ValorPorMesOut],
    summary="Valor CIF por mes",
)
@cached(cache)
def get_valor_por_mes(db: Session = Depends(get_db)):
    """
    Devuelve el total de valor CIF USD agrupado por mes (1-12).
    Resultados cacheados por 5 minutos.
    """
    results = (
        db.query(
            extract("month", Poliza.fecha_declaracion).label("mes"),
            func.sum(PolizaItem.valor_cif_uds).label("total_valor_cif_usd"),
        )
        .join(PolizaItem, Poliza.id == PolizaItem.poliza_id)
        .filter(Poliza.fecha_declaracion.isnot(None))
        .group_by(extract("month", Poliza.fecha_declaracion))
        .order_by(extract("month", Poliza.fecha_declaracion))
        .all()
    )

    return [
        ValorPorMesOut(mes=int(row.mes), total_valor_cif_usd=row.total_valor_cif_usd or 0.0)
        for row in results
    ]