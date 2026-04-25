import uuid

from pydantic import BaseModel, ConfigDict


class EspecieResponse(BaseModel):
    especie_id: uuid.UUID
    nombre_cientifico: str | None
    nombre_comun: str | None
    orden: str | None
    familia: str | None
    estado_conservacion: str | None

    model_config = ConfigDict(from_attributes=True)
