import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.ocurrencia import Ocurrencia


def create_ocurrencia(db: Session, ocurrencia: Ocurrencia) -> Ocurrencia:
    db.add(ocurrencia)
    db.commit()
    db.refresh(ocurrencia)
    return ocurrencia


def get_ocurrencias_by_salida(db: Session, salida_id: uuid.UUID) -> list[Ocurrencia]:
    stmt = (
        select(Ocurrencia)
        .options(joinedload(Ocurrencia.especie))
        .where(Ocurrencia.salida_id == salida_id)
        .order_by(Ocurrencia.fecha_hora.desc())
    )
    return list(db.scalars(stmt).all())


def get_ocurrencia_by_id(db: Session, ocurrencia_id: uuid.UUID) -> Ocurrencia | None:
    stmt = (
        select(Ocurrencia)
        .options(joinedload(Ocurrencia.especie))
        .where(Ocurrencia.id_ocurrencia == ocurrencia_id)
    )
    return db.scalar(stmt)

def update_ocurrencia(db: Session, ocurrencia: Ocurrencia) -> Ocurrencia:
    db.commit()
    db.refresh(ocurrencia)
    return ocurrencia


def delete_ocurrencia(db: Session, ocurrencia: Ocurrencia) -> None:
    db.delete(ocurrencia)
    db.commit()