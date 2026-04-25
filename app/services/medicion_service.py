from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.medicion import Medicion
from app.models.user import User
from app.repositories.medicion_repository import (
    create_medicion,
    get_medicion_by_ocurrencia_id,
    update_medicion,
)
from app.repositories.ocurrencia_repository import get_ocurrencia_by_id
from app.repositories.salida_repository import get_salida_by_id
from app.schemas.medicion import MedicionCreate, MedicionResponse, MedicionUpdate


def create_new_medicion(
    db: Session,
    data: MedicionCreate,
    current_user: User,
) -> MedicionResponse:
    ocurrencia = get_ocurrencia_by_id(db, data.ocurrencia_id)

    if not ocurrencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La ocurrencia no existe.",
        )

    salida = get_salida_by_id(db, ocurrencia.salida_id)
    if not salida or salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para crear medición en esta ocurrencia.",
        )

    existing = get_medicion_by_ocurrencia_id(db, data.ocurrencia_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La ocurrencia ya tiene una medición registrada.",
        )

    new_medicion = Medicion(
        medicion_id=data.medicion_id,
        ocurrencia_id=data.ocurrencia_id,
        oxigeno_disuelto_mg_l=data.oxigeno_disuelto_mg_l,
        ph=data.ph,
        turbidez_ntu=data.turbidez_ntu,
        conductividad_us_cm=data.conductividad_us_cm,
        tds_mg_l=data.tds_mg_l,
        temperatura_c=data.temperatura_c,
        transparencia_secchi_cm=data.transparencia_secchi_cm,
        nivel_estado_agua=data.nivel_estado_agua,
        orp_mv=data.orp_mv,
        alcalinidad_mg_l=data.alcalinidad_mg_l,
        dureza_mg_l=data.dureza_mg_l,
        salinidad=data.salinidad,
        amonio_mg_l=data.amonio_mg_l,
        fosforo_metales_mg_l=data.fosforo_metales_mg_l,
        nitratos_mg_l=data.nitratos_mg_l,
        nitritos_mg_l=data.nitritos_mg_l,
        fosfatos_mg_l=data.fosfatos_mg_l,
        clorofila_a_ug_l=data.clorofila_a_ug_l,
        sst_mg_l=data.sst_mg_l,
        coliformes_fecales_ufc=data.coliformes_fecales_ufc,
        observaciones=data.observaciones,
    )

    saved = create_medicion(db, new_medicion)
    return MedicionResponse.model_validate(saved)


def get_medicion_for_ocurrencia(
    db: Session,
    ocurrencia_id,
    current_user: User,
) -> MedicionResponse:
    ocurrencia = get_ocurrencia_by_id(db, ocurrencia_id)

    if not ocurrencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La ocurrencia no existe.",
        )

    salida = get_salida_by_id(db, ocurrencia.salida_id)
    if not salida or salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver esta medición.",
        )

    medicion = get_medicion_by_ocurrencia_id(db, ocurrencia_id)
    if not medicion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La ocurrencia no tiene medición registrada.",
        )

    return MedicionResponse.model_validate(medicion)

def update_existing_medicion(
    db: Session,
    ocurrencia_id,
    data: MedicionUpdate,
    current_user: User,
) -> MedicionResponse:
    ocurrencia = get_ocurrencia_by_id(db, ocurrencia_id)

    if not ocurrencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La ocurrencia no existe.",
        )

    salida = get_salida_by_id(db, ocurrencia.salida_id)
    if not salida or salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar esta medición.",
        )

    medicion = get_medicion_by_ocurrencia_id(db, ocurrencia_id)
    if not medicion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La ocurrencia no tiene medición registrada.",
        )

    fields = [
        "oxigeno_disuelto_mg_l",
        "ph",
        "turbidez_ntu",
        "conductividad_us_cm",
        "tds_mg_l",
        "temperatura_c",
        "transparencia_secchi_cm",
        "nivel_estado_agua",
        "orp_mv",
        "alcalinidad_mg_l",
        "dureza_mg_l",
        "salinidad",
        "amonio_mg_l",
        "fosforo_metales_mg_l",
        "nitratos_mg_l",
        "nitritos_mg_l",
        "fosfatos_mg_l",
        "clorofila_a_ug_l",
        "sst_mg_l",
        "coliformes_fecales_ufc",
        "observaciones",
    ]

    for field in fields:
        value = getattr(data, field)
        if value is not None:
            setattr(medicion, field, value)

    updated = update_medicion(db, medicion)
    return MedicionResponse.model_validate(updated)