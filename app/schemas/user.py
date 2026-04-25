import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    correo: EmailStr
    contrasena: str = Field(..., min_length=8, max_length=100)
    institucion: str | None = Field(default=None, max_length=150)


class UserResponse(BaseModel):
    usuario_id: uuid.UUID
    rol_id: int
    nombre: str | None
    correo: EmailStr | None
    institucion: str | None
    fecha_registro: datetime | None
    activo: bool

    model_config = ConfigDict(from_attributes=True)


class UserBasicInfo(BaseModel):
    usuario_id: uuid.UUID
    nombre: str | None
    correo: EmailStr | None

    model_config = ConfigDict(from_attributes=True)