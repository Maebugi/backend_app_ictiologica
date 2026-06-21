import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.estacion import Estacion

def create_estacion(
    db: Session,
    estacion: Estacion,
) -> Estacion:

    db.add(estacion)
    db.commit()
    db.refresh(estacion)

    return estacion
def get_estacion_by_id(
    db: Session,
    estacion_id: uuid.UUID,
) -> Estacion | None:

    stmt = (
        select(Estacion)
        .where(
            Estacion.estacion_id == estacion_id
        )
    )

    return db.scalar(stmt)
def get_estaciones(
    db: Session,
) -> list[Estacion]:

    stmt = (
        select(Estacion)
        .where(
            Estacion.activo == True
        )
        .order_by(
            Estacion.codigo.asc()
        )
    )

    return list(
        db.scalars(stmt).all()
    )
def get_estacion_by_codigo(
    db: Session,
    codigo: str,
) -> Estacion | None:

    stmt = (
        select(Estacion)
        .where(
            Estacion.codigo == codigo
        )
    )

    return db.scalar(stmt)