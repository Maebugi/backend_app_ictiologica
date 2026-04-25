import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SalidaCreate(BaseModel):
    salida_id: uuid.UUID
    nombre_lugar: str | None = Field(default=None, max_length=150)
    fecha_inicio: datetime | None = None
    observaciones: str | None = Field(default=None)


class SalidaResponse(BaseModel):
    salida_id: uuid.UUID
    id_usuario: uuid.UUID
    nombre_lugar: str | None
    fecha_inicio: datetime | None
    fecha_fin: datetime | None
    observaciones: str | None
    estado: str

    model_config = ConfigDict(from_attributes=True)


class SalidaFinishRequest(BaseModel):
    fecha_fin: datetime | None = None
    observaciones: str | None = None

class SalidaUpdate(BaseModel):
    nombre_lugar: str | None = Field(default=None, max_length=150)
    fecha_inicio: datetime | None = None
    fecha_fin: datetime | None = None
    observaciones: str | None = Field(default=None)
    estado: str | None = Field(default=None, max_length=20)