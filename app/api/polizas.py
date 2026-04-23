"""
Endpoints de Pólizas (CRUD):
  POST /polizas            - Crea una póliza con sus ítems (transacción atómica)
  GET  /polizas            - Lista pólizas con paginación
  GET  /polizas/{id}       - Detalle de una póliza con sus ítems

Todos los endpoints requieren autenticación JWT.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.db.database import get_db
from app.db.models import Poliza, PolizaItem, User
from app.schemas.poliza import (
    PolizaCreate,
    PolizaDetailOut,
    PolizaOut,
    PaginatedPolizas,
)
from app.core.security import get_current_user

router = APIRouter(
    prefix="/polizas",
    tags=["Pólizas"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=PolizaDetailOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear póliza con ítems (transacción atómica)",
)
def create_poliza(payload: PolizaCreate, db: Session = Depends(get_db)):
    """
    Crea una póliza (cabecera) y todos sus ítems dentro de una única transacción.
    Si cualquier ítem falla, se hace rollback de toda la operación para garantizar
    la integridad de los datos (principio ACID).
    """
    # Verificar que el correlativo no exista
    if db.query(Poliza).filter(Poliza.correlativo == payload.correlativo).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una póliza con correlativo {payload.correlativo}.",
        )

    try:
        # 1. Crear cabecera de póliza
        nueva_poliza = Poliza(
            correlativo=payload.correlativo,
            fecha_declaracion=payload.fecha_declaracion,
            tipo_cambio_dolar=payload.tipo_cambio_dolar,
            aduana_id=payload.aduana_id,
            tipo_regimen_id=payload.tipo_regimen_id,
        )
        db.add(nueva_poliza)
        db.flush()  # obtiene el ID sin hacer commit todavía

        # 2. Crear ítems asociados a la póliza
        for item_data in payload.items:
            item = PolizaItem(
                poliza_id=nueva_poliza.id,
                **item_data.model_dump(),
            )
            db.add(item)

        # 3. Commit atómico: cabecera + todos los ítems en una sola transacción
        db.commit()
        db.refresh(nueva_poliza)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la póliza: {str(e)}",
        )

    # Cargar relación de ítems para la respuesta
    db.refresh(nueva_poliza)
    return nueva_poliza


@router.get(
    "",
    response_model=PaginatedPolizas,
    summary="Listar pólizas (paginado)",
)
def list_polizas(
    limit: int = Query(default=20, ge=1, le=100, description="Resultados por página"),
    offset: int = Query(default=0, ge=0, description="Número de resultados a saltar"),
    db: Session = Depends(get_db),
):
    """
    Devuelve una lista paginada de pólizas (solo cabeceras, sin ítems).
    Usar GET /polizas/{id} para obtener los ítems de una póliza específica.
    """
    total = db.query(Poliza).count()
    polizas = db.query(Poliza).order_by(Poliza.id).offset(offset).limit(limit).all()

    return PaginatedPolizas(
        total=total,
        limit=limit,
        offset=offset,
        data=polizas,
    )


@router.get(
    "/{poliza_id}",
    response_model=PolizaDetailOut,
    summary="Obtener detalle de una póliza con sus ítems",
)
def get_poliza(poliza_id: int, db: Session = Depends(get_db)):
    """
    Devuelve la cabecera de una póliza junto con todos sus ítems.
    Usa un JOIN optimizado para obtener todo en una sola consulta a la DB.
    """
    poliza = (
        db.query(Poliza)
        .options(joinedload(Poliza.items))  # JOIN eficiente en una sola consulta
        .filter(Poliza.id == poliza_id)
        .first()
    )

    if not poliza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró la póliza con id {poliza_id}.",
        )

    return poliza
