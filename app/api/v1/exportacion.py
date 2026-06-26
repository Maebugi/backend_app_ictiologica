from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db

from app.models.user import User

from app.services.exportacion_service import (
    exportar_datos_service,
)

router = APIRouter(
    prefix="/exportacion",
    tags=["Exportación"],
)


@router.get("")
def exportar_datos_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    zip_path = exportar_datos_service(
        db,
        current_user,
    )

    return FileResponse(
        path=zip_path,
        filename="Exportacion_Ictiologica.zip",
        media_type="application/zip",
    )