from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.especie import Especie


def get_all_species(db: Session) -> list[Especie]:
    stmt = select(Especie).order_by(Especie.nombre_cientifico.asc())
    return list(db.scalars(stmt).all())


def search_species(db: Session, query: str) -> list[Especie]:
    stmt = (
        select(Especie)
        .where(
            (Especie.nombre_cientifico.ilike(f"%{query}%")) |
            (Especie.nombre_comun.ilike(f"%{query}%"))
        )
        .order_by(Especie.nombre_cientifico.asc())
    )
    return list(db.scalars(stmt).all())
