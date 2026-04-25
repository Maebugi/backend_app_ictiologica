import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.salida import Salida
from app.models.ocurrencia import Ocurrencia

def create_salida(db: Session, salida: Salida) -> Salida:
    db.add(salida)
    db.commit()
    db.refresh(salida)
    return salida


def update_salida(db: Session, salida: Salida) -> Salida:
    db.commit()
    db.refresh(salida)
    return salida


def get_salidas_by_user(db: Session, user_id: uuid.UUID) -> list[Salida]:
    stmt = (
        select(Salida)
        .where(Salida.id_usuario == user_id)
        .order_by(Salida.fecha_inicio.desc())
    )
    return list(db.scalars(stmt).all())


def get_salida_by_id(db: Session, salida_id: uuid.UUID) -> Salida | None:
    stmt = select(Salida).where(Salida.salida_id == salida_id)
    return db.scalar(stmt)

def count_ocurrencias_by_salida(db: Session, salida_id: uuid.UUID) -> int:
    stmt = select(Ocurrencia).where(Ocurrencia.salida_id == salida_id)
    return len(list(db.scalars(stmt).all()))


def delete_salida(db: Session, salida: Salida) -> None:
    db.delete(salida)
    db.commit()