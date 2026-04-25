from sqlalchemy.orm import Session

from app.repositories.especie_repository import get_all_species, search_species
from app.schemas.especie import EspecieResponse


def list_species(db: Session) -> list[EspecieResponse]:
    species = get_all_species(db)
    return [EspecieResponse.model_validate(specie) for specie in species]


def find_species(db: Session, query: str) -> list[EspecieResponse]:
    species = search_species(db, query)
    return [EspecieResponse.model_validate(specie) for specie in species]
