import uuid

from pydantic import BaseModel, ConfigDict


class SalidaEvidenciaResponse(BaseModel):
    id_foto: uuid.UUID
    salida_id: uuid.UUID
    ruta: str | None
    tipo_archivo: str | None
    observaciones: str | None

    model_config = ConfigDict(from_attributes=True)


class SalidaEvidenciaUpdate(BaseModel):
    observaciones: str | None = None