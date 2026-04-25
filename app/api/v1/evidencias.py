import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.evidencia import EvidenciaResponse, EvidenciaUpdate
from app.services.evidencia_service import (
    delete_evidencia_for_ocurrencia,
    list_evidencias_for_ocurrencia,
    update_evidencia_for_ocurrencia,
    upload_evidencia_for_ocurrencia,
)

router = APIRouter(prefix="/evidencias", tags=["Evidencias"])


@router.post("/upload", response_model=EvidenciaResponse)
def upload_evidencia_endpoint(
    ocurrencia_id: uuid.UUID = Form(...),
    observaciones: str | None = Form(default=None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return upload_evidencia_for_ocurrencia(
        db=db,
        ocurrencia_id=ocurrencia_id,
        observaciones=observaciones,
        file=file,
        current_user=current_user,
    )


@router.get("/ocurrencia/{ocurrencia_id}", response_model=list[EvidenciaResponse])
def list_evidencias_by_ocurrencia_endpoint(
    ocurrencia_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_evidencias_for_ocurrencia(db, ocurrencia_id, current_user)

@router.put("/{evidencia_id}", response_model=EvidenciaResponse)
def update_evidencia_endpoint(
    evidencia_id: uuid.UUID,
    data: EvidenciaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_evidencia_for_ocurrencia(db, evidencia_id, data, current_user)


@router.delete("/{evidencia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evidencia_endpoint(
    evidencia_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_evidencia_for_ocurrencia(db, evidencia_id, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)