import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.salida import Salida
from app.models.user import User
from app.repositories.salida_repository import (
    count_ocurrencias_by_salida,
    create_salida,
    delete_salida,
    get_salida_by_id,
    get_salidas_by_user,
    update_salida,
)


from app.schemas.salida import (
    SalidaCreate,
    SalidaFinishRequest,
    SalidaResponse,
    SalidaUpdate,
)


def build_salida_response(
    salida: Salida,
    db: Session,
) -> SalidaResponse:





    return SalidaResponse(
        salida_id=salida.salida_id,
        id_usuario=salida.id_usuario,
        nombre_lugar=salida.nombre_lugar,
        fecha_inicio=salida.fecha_inicio,
        fecha_fin=salida.fecha_fin,
        observaciones=salida.observaciones,
        estado=salida.estado,
        nombre_proyecto=salida.nombre_proyecto,

    )

def create_new_salida(
    db: Session,
    salida_data: SalidaCreate,
    current_user: User,
) -> SalidaResponse:

    existing_salida = get_salida_by_id(
        db,
        salida_data.salida_id,
    )

    if existing_salida:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una salida con ese identificador.",
        )

    colombia_tz = timezone(timedelta(hours=-5))

    new_salida = Salida(
        salida_id=salida_data.salida_id,
        id_usuario=current_user.usuario_id,
        nombre_lugar=salida_data.nombre_lugar,
        nombre_proyecto=salida_data.nombre_proyecto,
        fecha_inicio=salida_data.fecha_inicio
        or datetime.now(colombia_tz).replace(
            second=0,
            microsecond=0,
        ),
        observaciones=salida_data.observaciones,
        estado="abierta",
    )

    saved_salida = create_salida(
        db,
        new_salida,
    )

    return build_salida_response(
        saved_salida,
        db,
    )


def list_user_salidas(db: Session, current_user: User) -> list[SalidaResponse]:
    salidas = get_salidas_by_user(db, current_user.usuario_id)
    return [
    build_salida_response(
        salida,
        db,
    )
    for salida in salidas
]

 
def get_user_salida_detail(
    db: Session,
    salida_id: uuid.UUID,
    current_user: User,
) -> SalidaResponse:
    salida = get_salida_by_id(db, salida_id)

    if not salida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salida no encontrada.",
        )

    if salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta salida.",
        )

    return build_salida_response(
    salida,
    db,
)


def finish_user_salida(
    db: Session,
    salida_id: uuid.UUID,
    finish_data: SalidaFinishRequest,
    current_user: User,
) -> SalidaResponse:
    salida = get_salida_by_id(db, salida_id)

    if not salida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salida no encontrada.",
        )

    if salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta salida.",
        )

    if salida.estado == "cerrada":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La salida ya está finalizada.",
        )

    colombia_tz = timezone(timedelta(hours=-5))
    salida.fecha_fin = finish_data.fecha_fin or datetime.now(colombia_tz).replace(second=0, microsecond=0)

    if finish_data.observaciones is not None:
        salida.observaciones = finish_data.observaciones

    salida.estado = "cerrada"

    updated = update_salida(db, salida)

    return build_salida_response(
        updated,
        db,
    )

def update_user_salida(
    db: Session,
    salida_id: uuid.UUID,
    data: SalidaUpdate,
    current_user: User,
) -> SalidaResponse:
    salida = get_salida_by_id(db, salida_id)

    if not salida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salida no encontrada.",
        )

    if salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar esta salida.",
        )

    if data.nombre_lugar is not None:
        salida.nombre_lugar = data.nombre_lugar

    if data.fecha_inicio is not None:
        salida.fecha_inicio = data.fecha_inicio

    if data.fecha_fin is not None:
        salida.fecha_fin = data.fecha_fin

    if data.observaciones is not None:
        salida.observaciones = data.observaciones

    if data.estado is not None:
        salida.estado = data.estado
    
    if data.nombre_proyecto is not None:
        salida.nombre_proyecto = data.nombre_proyecto

    



    updated = update_salida(db, salida)

    return build_salida_response(
        updated,
        db,
    )


def delete_user_salida(
    db: Session,
    salida_id: uuid.UUID,
    current_user: User,
) -> None:
    salida = get_salida_by_id(db, salida_id)

    if not salida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Salida no encontrada.",
        )

    if salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta salida.",
        )

    total_ocurrencias = count_ocurrencias_by_salida(db, salida_id)
    if total_ocurrencias > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar una salida que tiene ocurrencias registradas.",
        )

    delete_salida(db, salida)