import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User

from app.schemas.salida_evidencia import (
    SalidaEvidenciaResponse,
    SalidaEvidenciaUpdate,
)

from app.services.salida_evidencia_service import (
    upload_evidencia_for_salida,
    list_evidencias_for_salida,
    update_evidencia_for_salida,
    delete_evidencia_for_salida,
)

router = APIRouter(
    prefix="/salida-evidencias",
    tags=["Salida Evidencias"],
)


@router.post(
    "/upload",
    response_model=SalidaEvidenciaResponse,
)
def upload_salida_evidencia_endpoint(
    salida_id: uuid.UUID = Form(...),
    observaciones: str | None = Form(default=None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return upload_evidencia_for_salida(
        db=db,
        salida_id=salida_id,
        observaciones=observaciones,
        file=file,
        current_user=current_user,
    )


@router.get(
    "/salida/{salida_id}",
    response_model=list[SalidaEvidenciaResponse],
)
def list_evidencias_by_salida_endpoint(
    salida_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_evidencias_for_salida(
        db,
        salida_id,
        current_user,
    )


@router.put(
    "/{evidencia_id}",
    response_model=SalidaEvidenciaResponse,
)
def update_salida_evidencia_endpoint(
    evidencia_id: uuid.UUID,
    data: SalidaEvidenciaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_evidencia_for_salida(
        db,
        evidencia_id,
        data,
        current_user,
    )


@router.delete(
    "/{evidencia_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_salida_evidencia_endpoint(
    evidencia_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_evidencia_for_salida(
        db,
        evidencia_id,
        current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )