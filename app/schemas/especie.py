import uuid

from pydantic import BaseModel, ConfigDict


class EspecieResponse(BaseModel):
    especie_id: uuid.UUID

    nombre_cientifico: str | None
    nombre_comun: str | None
    orden: str | None
    familia: str | None

    longitud_estandar: float | None
    talla_maxima: float | None
    peso_maximo: float | None

    longevidad: int | None

    habito_alimenticio: str | None
    reproductivo: str | None
    periodo_reproductivo: str | None

    estado_conservacion: str | None
    descripcion: str | None

    model_config = ConfigDict(from_attributes=True)