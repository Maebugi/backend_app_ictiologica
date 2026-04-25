import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.medicion import MedicionCreate, MedicionResponse, MedicionUpdate
from app.services.medicion_service import (
    create_new_medicion,
    get_medicion_for_ocurrencia,
    update_existing_medicion
)

router = APIRouter(prefix="/mediciones", tags=["Mediciones"])


@router.post("", response_model=MedicionResponse)
def create_medicion_endpoint(
    data: MedicionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_medicion(db, data, current_user)


@router.get("/ocurrencia/{ocurrencia_id}", response_model=MedicionResponse)
def get_medicion_by_ocurrencia_endpoint(
    ocurrencia_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_medicion_for_ocurrencia(db, ocurrencia_id, current_user)

@router.put("/ocurrencia/{ocurrencia_id}", response_model=MedicionResponse)
def update_medicion_by_ocurrencia_endpoint(
    ocurrencia_id: uuid.UUID,
    data: MedicionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_existing_medicion(db, ocurrencia_id, data, current_user)