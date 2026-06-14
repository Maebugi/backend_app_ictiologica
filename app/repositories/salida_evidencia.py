import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.salida_evidencia import SalidaEvidencia


def create_salida_evidencia(
    db: Session,
    evidencia: SalidaEvidencia,
) -> SalidaEvidencia:
    db.add(evidencia)
    db.commit()
    db.refresh(evidencia)
    return evidencia


def get_evidencias_by_salida(
    db: Session,
    salida_id: uuid.UUID,
) -> list[SalidaEvidencia]:
    stmt = (
        select(SalidaEvidencia)
        .where(SalidaEvidencia.salida_id == salida_id)
        .order_by(SalidaEvidencia.id_foto.desc())
    )
    return list(db.scalars(stmt).all())


def get_salida_evidencia_by_id(
    db: Session,
    evidencia_id: uuid.UUID,
) -> SalidaEvidencia | None:
    stmt = (
        select(SalidaEvidencia)
        .where(SalidaEvidencia.id_foto == evidencia_id)
    )
    return db.scalar(stmt)


def update_salida_evidencia(
    db: Session,
    evidencia: SalidaEvidencia,
) -> SalidaEvidencia:
    db.commit()
    db.refresh(evidencia)
    return evidencia


def delete_salida_evidencia(
    db: Session,
    evidencia: SalidaEvidencia,
) -> None:
    db.delete(evidencia)
    db.commit()


def delete_evidencias_by_salida(
    db: Session,
    salida_id: uuid.UUID,
) -> list[SalidaEvidencia]:
    evidencias = get_evidencias_by_salida(db, salida_id)

    for evidencia in evidencias:
        db.delete(evidencia)

    db.commit()

    return evidencias