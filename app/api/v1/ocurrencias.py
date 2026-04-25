import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.ocurrencia import (
    OcurrenciaCreate,
    OcurrenciaListItemResponse,
    OcurrenciaResponse,
    OcurrenciaUpdate,
)
from app.services.ocurrencia_service import (
    create_new_ocurrencia,
    delete_existing_ocurrencia,
    get_ocurrencia_detail,
    list_ocurrencias_for_salida,
    update_existing_ocurrencia,
)

router = APIRouter(prefix="/ocurrencias", tags=["Ocurrencias"])


@router.post("", response_model=OcurrenciaResponse)
def create_ocurrencia_endpoint(
    data: OcurrenciaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_ocurrencia(db, data, current_user)


@router.get("/salida/{salida_id}", response_model=list[OcurrenciaListItemResponse])
def list_ocurrencias_by_salida_endpoint(
    salida_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_ocurrencias_for_salida(db, salida_id, current_user)


@router.get("/{ocurrencia_id}", response_model=OcurrenciaResponse)
def get_ocurrencia_detail_endpoint(
    ocurrencia_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_ocurrencia_detail(db, ocurrencia_id, current_user)


@router.put("/{ocurrencia_id}", response_model=OcurrenciaResponse)
def update_ocurrencia_endpoint(
    ocurrencia_id: uuid.UUID,
    data: OcurrenciaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_existing_ocurrencia(db, ocurrencia_id, data, current_user)


@router.delete("/{ocurrencia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ocurrencia_endpoint(
    ocurrencia_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_existing_ocurrencia(db, ocurrencia_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)