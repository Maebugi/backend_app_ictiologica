import os
import shutil
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.evidencia_ocurrencia import EvidenciaOcurrencia
from app.models.user import User
from app.repositories.evidencia_repository import (
    create_evidencia,
    delete_evidencia,
    get_evidencia_by_id,
    get_evidencias_by_ocurrencia,
    update_evidencia,
)
from app.repositories.ocurrencia_repository import get_ocurrencia_by_id
from app.repositories.salida_repository import get_salida_by_id
from app.schemas.evidencia import EvidenciaResponse, EvidenciaUpdate


BASE_DIR = Path(__file__).resolve().parents[2]
EVIDENCIAS_DIR = BASE_DIR / "storage" / "evidencias"
EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)


def upload_evidencia_for_ocurrencia(
    db: Session,
    ocurrencia_id: uuid.UUID,
    observaciones: str | None,
    file: UploadFile,
    current_user: User,
) -> EvidenciaResponse:
    ocurrencia = get_ocurrencia_by_id(db, ocurrencia_id)

    if not ocurrencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La ocurrencia no existe.",
        )

    salida = get_salida_by_id(db, ocurrencia.salida_id)
    if not salida or salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para subir evidencias a esta ocurrencia.",
        )

    extension = Path(file.filename).suffix.lower() if file.filename else ".jpg"
    if extension not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de archivo no permitido. Usa jpg, jpeg, png o webp.",
        )

    evidencia_id = uuid.uuid4()
    filename = f"{evidencia_id}{extension}"
    file_path = EVIDENCIAS_DIR / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    relative_path = os.path.join("storage", "evidencias", filename).replace("\\", "/")

    evidencia = EvidenciaOcurrencia(
        id_foto=evidencia_id,
        id_ocurrencia=ocurrencia_id,
        ruta=relative_path,
        observaciones=observaciones,
    )

    saved = create_evidencia(db, evidencia)
    return EvidenciaResponse.model_validate(saved)


def list_evidencias_for_ocurrencia(
    db: Session,
    ocurrencia_id: uuid.UUID,
    current_user: User,
) -> list[EvidenciaResponse]:
    ocurrencia = get_ocurrencia_by_id(db, ocurrencia_id)

    if not ocurrencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La ocurrencia no existe.",
        )

    salida = get_salida_by_id(db, ocurrencia.salida_id)
    if not salida or salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver evidencias de esta ocurrencia.",
        )

    evidencias = get_evidencias_by_ocurrencia(db, ocurrencia_id)
    return [EvidenciaResponse.model_validate(item) for item in evidencias]

def update_evidencia_for_ocurrencia(
    db: Session,
    evidencia_id: uuid.UUID,
    data: EvidenciaUpdate,
    current_user: User,
) -> EvidenciaResponse:
    evidencia = get_evidencia_by_id(db, evidencia_id)

    if not evidencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidencia no encontrada.",
        )

    ocurrencia = get_ocurrencia_by_id(db, evidencia.id_ocurrencia)
    if not ocurrencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La ocurrencia no existe.",
        )

    salida = get_salida_by_id(db, ocurrencia.salida_id)
    if not salida or salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar esta evidencia.",
        )

    evidencia.observaciones = data.observaciones
    updated = update_evidencia(db, evidencia)
    return EvidenciaResponse.model_validate(updated)


def delete_evidencia_for_ocurrencia(
    db: Session,
    evidencia_id: uuid.UUID,
    current_user: User,
) -> None:
    evidencia = get_evidencia_by_id(db, evidencia_id)

    if not evidencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidencia no encontrada.",
        )

    ocurrencia = get_ocurrencia_by_id(db, evidencia.id_ocurrencia)
    if not ocurrencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La ocurrencia no existe.",
        )

    salida = get_salida_by_id(db, ocurrencia.salida_id)
    if not salida or salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta evidencia.",
        )

    if evidencia.ruta:
        file_path = BASE_DIR / evidencia.ruta
        if file_path.exists() and file_path.is_file():
            try:
                os.remove(file_path)
            except OSError:
                pass

    delete_evidencia(db, evidencia)