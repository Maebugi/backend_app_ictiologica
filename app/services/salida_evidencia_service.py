import os
import shutil
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.salida_evidencia import SalidaEvidencia
from app.models.user import User

from app.repositories.salida_evidencia import (
    create_salida_evidencia,
    delete_salida_evidencia,
    get_salida_evidencia_by_id,
    get_evidencias_by_salida,
    update_salida_evidencia,
)

from app.repositories.salida_repository import get_salida_by_id

from app.schemas.salida_evidencia import (
    SalidaEvidenciaResponse,
    SalidaEvidenciaUpdate,
)


BASE_DIR = Path(__file__).resolve().parents[2]

SALIDA_EVIDENCIAS_DIR = (
    BASE_DIR / "storage" / "salida_evidencias"
)

SALIDA_EVIDENCIAS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
def upload_evidencia_for_salida(
    db: Session,
    salida_id: uuid.UUID,
    observaciones: str | None,
    file: UploadFile,
    current_user: User,
) -> SalidaEvidenciaResponse:

    salida = get_salida_by_id(db, salida_id)

    if not salida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La salida no existe.",
        )

    if salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para esta salida.",
        )

    extension = (
        Path(file.filename).suffix.lower()
        if file.filename
        else ".jpg"
    )

    if extension not in [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".mp4",
        ".mov",
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato no permitido.",
        )

    evidencia_id = uuid.uuid4()

    codigo_base = (
    salida.nombre_proyecto
    or salida.nombre_lugar
    or str(salida.salida_id)
    )

    codigo_base = (
    str(codigo_base)
    .replace(" ", "_")
    .replace("/", "_")
    )
    filename = (
    f"{codigo_base}_F{datetime.now():%Y%m%d}"
    f"_H{datetime.now():%H%M%S}"
    f"{extension}"
    )

    file_path = SALIDA_EVIDENCIAS_DIR / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    relative_path = (
        os.path.join(
            "storage",
            "salida_evidencias",
            filename,
        )
        .replace("\\", "/")
    )

    evidencia = SalidaEvidencia(
        id_foto=evidencia_id,
        salida_id=salida_id,
        ruta=relative_path,
        tipo_archivo="video"
        if extension in [".mp4", ".mov"]
        else "foto",
        observaciones=observaciones,
    )

    saved = create_salida_evidencia(
        db,
        evidencia,
    )

    return SalidaEvidenciaResponse.model_validate(
        saved
    )

def list_evidencias_for_salida(
    db: Session,
    salida_id: uuid.UUID,
    current_user: User,
) -> list[SalidaEvidenciaResponse]:

    salida = get_salida_by_id(db, salida_id)

    if not salida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La salida no existe.",
        )

    if salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver estas evidencias.",
        )

    evidencias = get_evidencias_by_salida(
        db,
        salida_id,
    )

    return [
        SalidaEvidenciaResponse.model_validate(item)
        for item in evidencias
    ]


def update_evidencia_for_salida(
    db: Session,
    evidencia_id: uuid.UUID,
    data: SalidaEvidenciaUpdate,
    current_user: User,
) -> SalidaEvidenciaResponse:

    evidencia = get_salida_evidencia_by_id(
        db,
        evidencia_id,
    )

    if not evidencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidencia no encontrada.",
        )

    salida = get_salida_by_id(
        db,
        evidencia.salida_id,
    )

    if not salida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La salida no existe.",
        )

    if salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar esta evidencia.",
        )

    evidencia.observaciones = data.observaciones

    updated = update_salida_evidencia(
        db,
        evidencia,
    )

    return SalidaEvidenciaResponse.model_validate(
        updated
    )



def delete_evidencia_for_salida(
    db: Session,
    evidencia_id: uuid.UUID,
    current_user: User,
) -> None:

    evidencia = get_salida_evidencia_by_id(
        db,
        evidencia_id,
    )

    if not evidencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidencia no encontrada.",
        )

    salida = get_salida_by_id(
        db,
        evidencia.salida_id,
    )

    if not salida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La salida no existe.",
        )

    if salida.id_usuario != current_user.usuario_id:
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

    delete_salida_evidencia(
        db,
        evidencia,
    )