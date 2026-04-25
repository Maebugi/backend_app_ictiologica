import uuid

from pydantic import BaseModel, ConfigDict


class EvidenciaResponse(BaseModel):
    id_foto: uuid.UUID
    id_ocurrencia: uuid.UUID
    ruta: str | None
    observaciones: str | None

    model_config = ConfigDict(from_attributes=True)

class EvidenciaUpdate(BaseModel):
    observaciones: str | None = None