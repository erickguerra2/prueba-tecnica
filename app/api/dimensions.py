"""
Endpoints de dimensiones (tablas lookup):
  GET /dimensions/aduanas         - Lista todas las aduanas
  GET /dimensions/paises          - Lista todos los países
  GET /dimensions/regimenes       - Lista todos los tipos de régimen
  GET /dimensions/sac             - Lista las fracciones SAC (paginado)
  GET /dimensions/unidades-medida - Lista los tipos de unidad de medida

Todos los endpoints requieren autenticación JWT.
"""
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Aduana, Pais, TipoRegimen, SAC, TipoUnidadMedida, User
from app.schemas.dimension import DimensionOut, SACOut
from app.core.security import get_current_user

router = APIRouter(
    prefix="/dimensions",
    tags=["Dimensiones"],
    dependencies=[Depends(get_current_user)],  # todas las rutas requieren JWT
)


@router.get(
    "/aduanas",
    response_model=List[DimensionOut],
    summary="Listar aduanas",
)
def get_aduanas(db: Session = Depends(get_db)):
    """Devuelve la lista completa de aduanas registradas."""
    return db.query(Aduana).order_by(Aduana.name).all()


@router.get(
    "/paises",
    response_model=List[DimensionOut],
    summary="Listar países",
)
def get_paises(db: Session = Depends(get_db)):
    """Devuelve la lista completa de países registrados."""
    return db.query(Pais).order_by(Pais.name).all()


@router.get(
    "/regimenes",
    response_model=List[DimensionOut],
    summary="Listar tipos de régimen",
)
def get_regimenes(db: Session = Depends(get_db)):
    """Devuelve la lista completa de tipos de régimen aduanero."""
    return db.query(TipoRegimen).order_by(TipoRegimen.name).all()


@router.get(
    "/unidades-medida",
    response_model=List[DimensionOut],
    summary="Listar unidades de medida",
)
def get_unidades_medida(db: Session = Depends(get_db)):
    """Devuelve la lista completa de tipos de unidad de medida."""
    return db.query(TipoUnidadMedida).order_by(TipoUnidadMedida.name).all()


@router.get(
    "/sac",
    response_model=List[SACOut],
    summary="Listar fracciones SAC (paginado)",
)
def get_sac(
    limit: int = Query(default=50, ge=1, le=500, description="Cantidad de resultados"),
    offset: int = Query(default=0, ge=0, description="Número de resultados a saltar"),
    db: Session = Depends(get_db),
):
    """
    Devuelve las fracciones SAC (Sistema Arancelario Centroamericano).
    Paginado porque hay miles de registros.
    """
    return db.query(SAC).order_by(SAC.fraccion).offset(offset).limit(limit).all()
