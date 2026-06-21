import uuid

from pydantic import BaseModel


class EstacionCreate(BaseModel):
    codigo: str
    nombre: str
    cuerpo_agua: str
    latitud: float
    longitud: float


class EstacionUpdate(BaseModel):
    codigo: str | None = None
    nombre: str | None = None
    cuerpo_agua: str | None = None
    latitud: float | None = None
    longitud: float | None = None
    activo: bool | None = None


class EstacionResponse(BaseModel):
    estacion_id: uuid.UUID
    codigo: str
    nombre: str
    cuerpo_agua: str
    latitud: float
    longitud: float
    activo: bool

    model_config = {
        "from_attributes": True
    }

class EstacionNearestResponse(
    BaseModel,
):
    estacion_id: uuid.UUID
    codigo: str
    nombre: str
    cuerpo_agua: str

    distancia_metros: float

    model_config = {
        "from_attributes": True
    }