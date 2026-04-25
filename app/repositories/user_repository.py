import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User


def get_user_by_email(db: Session, correo: str) -> User | None:
    stmt = select(User).where(User.correo == correo)
    return db.scalar(stmt)


def get_user_by_id(db: Session, usuario_id: uuid.UUID) -> User | None:
    stmt = select(User).where(User.usuario_id == usuario_id)
    return db.scalar(stmt)


def get_role_by_name(db: Session, nombre_rol: str) -> Role | None:
    stmt = select(Role).where(Role.nombre_rol == nombre_rol)
    return db.scalar(stmt)


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user