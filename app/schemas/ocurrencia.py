import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OcurrenciaCreate(BaseModel):
    id_ocurrencia: uuid.UUID
    id_especie: uuid.UUID
    salida_id: uuid.UUID

    fecha_hora: datetime | None = None
    coordenadas: str | None = Field(default=None, max_length=50)
    altitud: float | None = None
    esfuerzo: float | None = None
    cpue: float | None = None
    longitud_pez: float | None = None
    peso: float | None = None
    sexo: str | None = Field(default=None, max_length=20)
    estado_ontogenetico: str | None = Field(default=None, max_length=30)
    estadio_vida: str | None = Field(default=None, max_length=30)
    condicion_reproductiva: str | None = Field(default=None, max_length=30)
    comportamiento: str | None = Field(default=None, max_length=50)
    anomalias: str | None = None
    mortalidad: str | None = Field(default=None, max_length=30)
    vouchers: str | None = Field(default=None, max_length=100)
    nivel_certeza: int | None = None
    ancho_cauce: float | None = None
    profundidad_media: float | None = None
    profundidad_maxima: float | None = None
    caudal_velocidad: float | None = None
    tipo_habitat: str | None = Field(default=None, max_length=50)
    microhabitat: str | None = Field(default=None, max_length=50)
    cobertura_dosel: float | None = None
    uso_suelo_ribereno: str | None = Field(default=None, max_length=50)
    estabilidad_orillas: str | None = Field(default=None, max_length=50)
    sustrato: str | None = Field(default=None, max_length=50)
    clima: str | None = Field(default=None, max_length=50)
    metodo_captura: str | None = Field(default=None, max_length=50)
    arte_pesca: str | None = Field(default=None, max_length=50)
    codigo_muestreo: str | None = Field(default=None, max_length=50)
    datum: str | None = Field(default=None, max_length=20)
    observaciones: str | None = None


class OcurrenciaResponse(BaseModel):
    id_ocurrencia: uuid.UUID
    id_especie: uuid.UUID
    salida_id: uuid.UUID
    fecha_hora: datetime | None
    coordenadas: str | None
    altitud: float | None
    esfuerzo: float | None
    cpue: float | None
    longitud_pez: float | None
    peso: float | None
    sexo: str | None
    estado_ontogenetico: str | None
    estadio_vida: str | None
    condicion_reproductiva: str | None
    comportamiento: str | None
    anomalias: str | None
    mortalidad: str | None
    vouchers: str | None
    nivel_certeza: int | None
    ancho_cauce: float | None
    profundidad_media: float | None
    profundidad_maxima: float | None
    caudal_velocidad: float | None
    tipo_habitat: str | None
    microhabitat: str | None
    cobertura_dosel: float | None
    uso_suelo_ribereno: str | None
    estabilidad_orillas: str | None
    sustrato: str | None
    clima: str | None
    metodo_captura: str | None
    arte_pesca: str | None
    codigo_muestreo: str | None
    datum: str | None
    observaciones: str | None
    nombre_comun: str | None = None
    nombre_cientifico: str | None = None
    familia: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


class OcurrenciaListItemResponse(BaseModel):
    id_ocurrencia: uuid.UUID
    id_especie: uuid.UUID
    fecha_hora: datetime | None
    sexo: str | None
    longitud_pez: float | None
    peso: float | None
    observaciones: str | None

    nombre_comun: str | None = None
    nombre_cientifico: str | None = None
    familia: str | None = None

    model_config = ConfigDict(from_attributes=True)

class OcurrenciaUpdate(BaseModel):
    id_especie: uuid.UUID | None = None
    fecha_hora: datetime | None = None
    coordenadas: str | None = Field(default=None, max_length=50)
    altitud: float | None = None
    esfuerzo: float | None = None
    cpue: float | None = None
    longitud_pez: float | None = None
    peso: float | None = None
    sexo: str | None = Field(default=None, max_length=20)
    estado_ontogenetico: str | None = Field(default=None, max_length=30)
    estadio_vida: str | None = Field(default=None, max_length=30)
    condicion_reproductiva: str | None = Field(default=None, max_length=30)
    comportamiento: str | None = Field(default=None, max_length=50)
    anomalias: str | None = None
    mortalidad: str | None = Field(default=None, max_length=30)
    vouchers: str | None = Field(default=None, max_length=100)
    nivel_certeza: int | None = None
    ancho_cauce: float | None = None
    profundidad_media: float | None = None
    profundidad_maxima: float | None = None
    caudal_velocidad: float | None = None
    tipo_habitat: str | None = Field(default=None, max_length=50)
    microhabitat: str | None = Field(default=None, max_length=50)
    cobertura_dosel: float | None = None
    uso_suelo_ribereno: str | None = Field(default=None, max_length=50)
    estabilidad_orillas: str | None = Field(default=None, max_length=50)
    sustrato: str | None = Field(default=None, max_length=50)
    clima: str | None = Field(default=None, max_length=50)
    metodo_captura: str | None = Field(default=None, max_length=50)
    arte_pesca: str | None = Field(default=None, max_length=50)
    codigo_muestreo: str | None = Field(default=None, max_length=50)
    datum: str | None = Field(default=None, max_length=20)
    observaciones: str | None = None