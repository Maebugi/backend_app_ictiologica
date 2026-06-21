import uuid

from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.models.estacion import Estacion

from app.utils.geolocation import ( haversine_distance,)
from app.schemas.estacion import (EstacionNearestResponse,)

from app.schemas.estacion import (
    EstacionCreate,
    EstacionResponse,
)

from app.repositories.estacion_repository import (
    create_estacion,
    get_estacion_by_codigo,
    get_estacion_by_id,
    get_estaciones,
)
MAX_DISTANCE_METERS = 10000

def find_nearest_estacion(
    db: Session,
    latitud: float,
    longitud: float,
) -> Estacion:

    estaciones = get_estaciones(db)

    if not estaciones:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existen estaciones registradas.",
        )

    nearest = None
    nearest_distance = None

    for estacion in estaciones:

        distance = haversine_distance(
            latitud,
            longitud,
            estacion.latitud,
            estacion.longitud,
        )

        if (
            nearest_distance is None
            or distance < nearest_distance
        ):
            nearest = estacion
            nearest_distance = distance

    if nearest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No fue posible determinar una estación.",
        )

    print(
    nearest.codigo,
    nearest.nombre,
    nearest_distance
    )
    if nearest_distance > MAX_DISTANCE_METERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "mensaje": (
                    f"No existe una estación dentro de "
                    f"{MAX_DISTANCE_METERS} metros "
                    f"de la ubicación actual."
                ),
                "estacion_mas_cercana": nearest.codigo,
                "nombre_estacion": nearest.nombre,
                "cuerpo_agua": nearest.cuerpo_agua,
                "distancia_metros": round(
                    nearest_distance,
                    2,
                ),
            },
        )

    return nearest

def create_estacion_service(
    db: Session,
    data: EstacionCreate,
) -> EstacionResponse:

    existing = get_estacion_by_codigo(
        db,
        data.codigo,
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una estación con ese código.",
        )
    estacion = Estacion(
        codigo=data.codigo,
        nombre=data.nombre,
        cuerpo_agua=data.cuerpo_agua,
        latitud=data.latitud,
        longitud=data.longitud,
    )
    saved = create_estacion(
        db,
        estacion,
    )

    return EstacionResponse.model_validate(
        saved
    )
def list_estaciones_service(
    db: Session,
) -> list[EstacionResponse]:

    estaciones = get_estaciones(db)

    return [
        EstacionResponse.model_validate(
            item
        )
        for item in estaciones
    ]
def get_nearest_estacion_service(
    db: Session,
    latitud: float,
    longitud: float,
) -> EstacionNearestResponse:

    nearest = find_nearest_estacion(
        db,
        latitud,
        longitud,
    )

    distance = haversine_distance(
        latitud,
        longitud,
        nearest.latitud,
        nearest.longitud,
    )

    return EstacionNearestResponse(
        estacion_id=nearest.estacion_id,
        codigo=nearest.codigo,
        nombre=nearest.nombre,
        cuerpo_agua=nearest.cuerpo_agua,
        distancia_metros=round(
            distance,
            2,
        ),
    )