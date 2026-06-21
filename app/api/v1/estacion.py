from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.estacion import (
    EstacionCreate,
    EstacionResponse,
)
from app.schemas.estacion import (EstacionNearestResponse,)
from app.services.estacion_service import (get_nearest_estacion_service,)

from app.services.estacion_service import (
    create_estacion_service,
    list_estaciones_service,
)

router = APIRouter(
    prefix="/estaciones",
    tags=["Estaciones"],
)
@router.post(
    "",
    response_model=EstacionResponse,
)
def create_estacion_endpoint(
    data: EstacionCreate,
    db: Session = Depends(get_db),
):
    return create_estacion_service(
        db,
        data,
    )
@router.get(
    "",
    response_model=list[EstacionResponse],
)
def list_estaciones_endpoint(
    db: Session = Depends(get_db),
):
    return list_estaciones_service(
        db,
    )
@router.get(
    "/nearest",
    response_model=EstacionNearestResponse,
)
def get_nearest_estacion_endpoint(
    latitud: float,
    longitud: float,
    db: Session = Depends(get_db),
):
    return get_nearest_estacion_service(
        db,
        latitud,
        longitud,
    )