import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medicion import Medicion


def create_medicion(db: Session, medicion: Medicion) -> Medicion:
    db.add(medicion)
    db.commit()
    db.refresh(medicion)
    return medicion


def get_medicion_by_ocurrencia_id(db: Session, ocurrencia_id: uuid.UUID) -> Medicion | None:
    stmt = select(Medicion).where(Medicion.ocurrencia_id == ocurrencia_id)
    return db.scalar(stmt)

def delete_medicion(db: Session, medicion: Medicion) -> None:
    db.delete(medicion)
    db.commit()


def update_medicion(db: Session, medicion: Medicion) -> Medicion:
    db.commit()
    db.refresh(medicion)
    return medicion