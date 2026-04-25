import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.evidencia_ocurrencia import EvidenciaOcurrencia


def create_evidencia(db: Session, evidencia: EvidenciaOcurrencia) -> EvidenciaOcurrencia:
    db.add(evidencia)
    db.commit()
    db.refresh(evidencia)
    return evidencia


def get_evidencias_by_ocurrencia(db: Session, ocurrencia_id: uuid.UUID) -> list[EvidenciaOcurrencia]:
    stmt = (
        select(EvidenciaOcurrencia)
        .where(EvidenciaOcurrencia.id_ocurrencia == ocurrencia_id)
        .order_by(EvidenciaOcurrencia.id_foto.desc())
    )
    return list(db.scalars(stmt).all())

def get_evidencia_by_id(db: Session, evidencia_id: uuid.UUID) -> EvidenciaOcurrencia | None:
    stmt = select(EvidenciaOcurrencia).where(EvidenciaOcurrencia.id_foto == evidencia_id)
    return db.scalar(stmt)


def delete_evidencia(db: Session, evidencia: EvidenciaOcurrencia) -> None:
    db.delete(evidencia)
    db.commit()


def delete_evidencias_by_ocurrencia(db: Session, ocurrencia_id: uuid.UUID) -> list[EvidenciaOcurrencia]:
    evidencias = get_evidencias_by_ocurrencia(db, ocurrencia_id)
    for evidencia in evidencias:
        db.delete(evidencia)
    db.commit()
    return evidencias

def update_evidencia(db: Session, evidencia: EvidenciaOcurrencia) -> EvidenciaOcurrencia:
    db.commit()
    db.refresh(evidencia)
    return evidencia

def delete_evidencia(db: Session, evidencia: EvidenciaOcurrencia) -> None:
    db.delete(evidencia)
    db.commit()