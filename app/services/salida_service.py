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


def create_new_salida(
    db: Session,
    salida_data: SalidaCreate,
    current_user: User,
) -> SalidaResponse:
    existing_salida = get_salida_by_id(db, salida_data.salida_id)
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
        fecha_inicio=salida_data.fecha_inicio or datetime.now(colombia_tz).replace(second=0, microsecond=0),
        observaciones=salida_data.observaciones,
        estado="abierta",
    )

    saved_salida = create_salida(db, new_salida)
    return SalidaResponse.model_validate(saved_salida)


def list_user_salidas(db: Session, current_user: User) -> list[SalidaResponse]:
    salidas = get_salidas_by_user(db, current_user.usuario_id)
    return [SalidaResponse.model_validate(salida) for salida in salidas]


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

    return SalidaResponse.model_validate(salida)


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
    return SalidaResponse.model_validate(updated)


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

    updated = update_salida(db, salida)
    return SalidaResponse.model_validate(updated)


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