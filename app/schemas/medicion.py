import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MedicionCreate(BaseModel):
    medicion_id: uuid.UUID
    ocurrencia_id: uuid.UUID

    oxigeno_disuelto_mg_l: Decimal | None = None
    ph: Decimal | None = None
    turbidez_ntu: Decimal | None = None
    conductividad_us_cm: Decimal | None = None
    tds_mg_l: Decimal | None = None
    temperatura_c: Decimal | None = None
    transparencia_secchi_cm: Decimal | None = None
    nivel_estado_agua: str | None = Field(default=None, max_length=50)
    orp_mv: Decimal | None = None
    alcalinidad_mg_l: Decimal | None = None
    dureza_mg_l: Decimal | None = None
    salinidad: Decimal | None = None
    amonio_mg_l: Decimal | None = None
    fosforo_metales_mg_l: Decimal | None = None
    nitratos_mg_l: Decimal | None = None
    nitritos_mg_l: Decimal | None = None
    fosfatos_mg_l: Decimal | None = None
    clorofila_a_ug_l: Decimal | None = None
    sst_mg_l: Decimal | None = None
    coliformes_fecales_ufc: int | None = None
    observaciones: str | None = None


class MedicionResponse(BaseModel):
    medicion_id: uuid.UUID
    ocurrencia_id: uuid.UUID

    oxigeno_disuelto_mg_l: Decimal | None
    ph: Decimal | None
    turbidez_ntu: Decimal | None
    conductividad_us_cm: Decimal | None
    tds_mg_l: Decimal | None
    temperatura_c: Decimal | None
    transparencia_secchi_cm: Decimal | None
    nivel_estado_agua: str | None
    orp_mv: Decimal | None
    alcalinidad_mg_l: Decimal | None
    dureza_mg_l: Decimal | None
    salinidad: Decimal | None
    amonio_mg_l: Decimal | None
    fosforo_metales_mg_l: Decimal | None
    nitratos_mg_l: Decimal | None
    nitritos_mg_l: Decimal | None
    fosfatos_mg_l: Decimal | None
    clorofila_a_ug_l: Decimal | None
    sst_mg_l: Decimal | None
    coliformes_fecales_ufc: int | None
    observaciones: str | None

    model_config = ConfigDict(from_attributes=True)

class MedicionUpdate(BaseModel):
    oxigeno_disuelto_mg_l: Decimal | None = None
    ph: Decimal | None = None
    turbidez_ntu: Decimal | None = None
    conductividad_us_cm: Decimal | None = None
    tds_mg_l: Decimal | None = None
    temperatura_c: Decimal | None = None
    transparencia_secchi_cm: Decimal | None = None
    nivel_estado_agua: str | None = Field(default=None, max_length=50)
    orp_mv: Decimal | None = None
    alcalinidad_mg_l: Decimal | None = None
    dureza_mg_l: Decimal | None = None
    salinidad: Decimal | None = None
    amonio_mg_l: Decimal | None = None
    fosforo_metales_mg_l: Decimal | None = None
    nitratos_mg_l: Decimal | None = None
    nitritos_mg_l: Decimal | None = None
    fosfatos_mg_l: Decimal | None = None
    clorofila_a_ug_l: Decimal | None = None
    sst_mg_l: Decimal | None = None
    coliformes_fecales_ufc: int | None = None
    observaciones: str | None = None