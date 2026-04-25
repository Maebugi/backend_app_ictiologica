import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.salida import SalidaCreate, SalidaFinishRequest, SalidaResponse, SalidaUpdate
from app.services.salida_service import (
    create_new_salida,
    finish_user_salida,
    get_user_salida_detail,
    list_user_salidas,
    update_user_salida,
    delete_user_salida
)

router = APIRouter(prefix="/salidas", tags=["Salidas"])


@router.post("", response_model=SalidaResponse)
def create_salida_endpoint(
    salida_data: SalidaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_salida(db, salida_data, current_user)


@router.get("", response_model=list[SalidaResponse])
def list_salidas_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_user_salidas(db, current_user)


@router.get("/{salida_id}", response_model=SalidaResponse)
def get_salida_detail_endpoint(
    salida_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_salida_detail(db, salida_id, current_user)


@router.put("/{salida_id}/finalizar", response_model=SalidaResponse)
def finish_salida_endpoint(
    salida_id: uuid.UUID,
    finish_data: SalidaFinishRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return finish_user_salida(db, salida_id, finish_data, current_user)


@router.put("/{salida_id}", response_model=SalidaResponse)
def update_salida_endpoint(
    salida_id: uuid.UUID,
    data: SalidaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_user_salida(db, salida_id, data, current_user)


@router.delete("/{salida_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_salida_endpoint(
    salida_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_user_salida(db, salida_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)