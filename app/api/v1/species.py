from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.especie import EspecieResponse
from app.services.especie_service import find_species, list_species

router = APIRouter(prefix="/species", tags=["Species"])


@router.get("", response_model=list[EspecieResponse])
def get_species(db: Session = Depends(get_db)):
    return list_species(db)


@router.get("/search", response_model=list[EspecieResponse])
def search_species_endpoint(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    return find_species(db, q)
