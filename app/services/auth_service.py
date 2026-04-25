import uuid
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_role_by_name,
    get_user_by_email,
)
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.utils.constants import DEFAULT_RESEARCHER_ROLE, TOKEN_TYPE


def register_user(db: Session, user_data: UserCreate) -> User:
    existing_user = get_user_by_email(db, user_data.correo)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado.",
        )

    researcher_role = get_role_by_name(db, DEFAULT_RESEARCHER_ROLE)
    if not researcher_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No existe el rol Investigador en la base de datos.",
        )
    colombia_tz = timezone(timedelta(hours=-5))
    new_user = User(
        usuario_id=uuid.uuid4(),
        rol_id=researcher_role.rol_id,
        nombre=user_data.nombre,
        correo=user_data.correo,
        contrasena=hash_password(user_data.contrasena),
        institucion=user_data.institucion,
        fecha_registro=datetime.now(timezone.utc).replace(microsecond=0),
        activo=True,
    )

    return create_user(db, new_user)


def login_user(db: Session, credentials: LoginRequest) -> TokenResponse:
    user = get_user_by_email(db, credentials.correo)

    if not user or not user.contrasena:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
        )

    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está inactivo.",
        )

    if not verify_password(credentials.contrasena, user.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
        )

    access_token = create_access_token(subject=str(user.usuario_id))

    return TokenResponse(
        access_token=access_token,
        token_type=TOKEN_TYPE,
        user={
            "usuario_id": user.usuario_id,
            "nombre": user.nombre,
            "correo": user.correo,
        },
    )
def get_me(current_user: User) -> UserResponse:
    return UserResponse.model_validate(current_user)