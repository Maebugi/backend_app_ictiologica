from pydantic import BaseModel, EmailStr

from app.schemas.user import UserBasicInfo


class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserBasicInfo