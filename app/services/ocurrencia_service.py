import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ocurrencia import Ocurrencia
from app.models.user import User
from app.repositories.especie_repository import get_all_species
from app.repositories.ocurrencia_repository import (
    create_ocurrencia,
    delete_ocurrencia,
    get_ocurrencia_by_id,
    get_ocurrencias_by_salida,
    delete_ocurrencia,
    update_ocurrencia
)
from app.repositories.salida_repository import get_salida_by_id
from app.schemas.ocurrencia import (
    OcurrenciaCreate,
    OcurrenciaListItemResponse,
    OcurrenciaResponse,
    OcurrenciaUpdate,
)
from app.repositories.evidencia_repository import delete_evidencias_by_ocurrencia
from app.repositories.medicion_repository import delete_medicion, get_medicion_by_ocurrencia_id

BASE_DIR = Path(__file__).resolve().parents[2]

def create_new_ocurrencia(
    db: Session,
    data: OcurrenciaCreate,
    current_user: User,
) -> OcurrenciaResponse:
    salida = get_salida_by_id(db, data.salida_id)

    if not salida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La salida no existe.",
        )

    if salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para agregar ocurrencias a esta salida.",
        )

    if salida.estado == "cerrada":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes agregar ocurrencias a una salida cerrada.",
        )

    especies = get_all_species(db)
    especie_ids = {especie.especie_id for especie in especies}

    if data.id_especie not in especie_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La especie seleccionada no existe en el catálogo.",
        )

    colombia_tz = timezone(timedelta(hours=-5))

    new_ocurrencia = Ocurrencia(
        id_ocurrencia=data.id_ocurrencia,
        id_especie=data.id_especie,
        salida_id=data.salida_id,
        fecha_hora=data.fecha_hora or datetime.now(colombia_tz).replace(second=0, microsecond=0),
        coordenadas=data.coordenadas,
        altitud=data.altitud,
        esfuerzo=data.esfuerzo,
        cpue=data.cpue,
        longitud_pez=data.longitud_pez,
        peso=data.peso,
        sexo=data.sexo,
        estado_ontogenetico=data.estado_ontogenetico,
        estadio_vida=data.estadio_vida,
        condicion_reproductiva=data.condicion_reproductiva,
        comportamiento=data.comportamiento,
        anomalias=data.anomalias,
        mortalidad=data.mortalidad,
        vouchers=data.vouchers,
        nivel_certeza=data.nivel_certeza,
        ancho_cauce=data.ancho_cauce,
        profundidad_media=data.profundidad_media,
        profundidad_maxima=data.profundidad_maxima,
        caudal_velocidad=data.caudal_velocidad,
        tipo_habitat=data.tipo_habitat,
        microhabitat=data.microhabitat,
        cobertura_dosel=data.cobertura_dosel,
        uso_suelo_ribereno=data.uso_suelo_ribereno,
        estabilidad_orillas=data.estabilidad_orillas,
        sustrato=data.sustrato,
        clima=data.clima,
        metodo_captura=data.metodo_captura,
        arte_pesca=data.arte_pesca,
        codigo_muestreo=data.codigo_muestreo,
        datum=data.datum,
        observaciones=data.observaciones,
    )

    saved = create_ocurrencia(db, new_ocurrencia)
    return OcurrenciaResponse.model_validate(saved)


def list_ocurrencias_for_salida(
    db: Session,
    salida_id,
    current_user: User,
) -> list[OcurrenciaListItemResponse]:
    salida = get_salida_by_id(db, salida_id)

    if not salida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La salida no existe.",
        )

    if salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver ocurrencias de esta salida.",
        )

    ocurrencias = get_ocurrencias_by_salida(db, salida_id)

    response = []
    for item in ocurrencias:
        response.append(
            OcurrenciaListItemResponse(
                id_ocurrencia=item.id_ocurrencia,
                id_especie=item.id_especie,
                fecha_hora=item.fecha_hora,
                sexo=item.sexo,
                longitud_pez=item.longitud_pez,
                peso=item.peso,
                observaciones=item.observaciones,
                nombre_comun=item.especie.nombre_comun if item.especie else None,
                nombre_cientifico=item.especie.nombre_cientifico if item.especie else None,
                familia=item.especie.familia if item.especie else None,
            )
        )

    return response


def get_ocurrencia_detail(
    db: Session,
    ocurrencia_id,
    current_user: User,
) -> OcurrenciaResponse:
    ocurrencia = get_ocurrencia_by_id(db, ocurrencia_id)

    if not ocurrencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ocurrencia no encontrada.",
        )

    salida = get_salida_by_id(db, ocurrencia.salida_id)

    if not salida or salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta ocurrencia.",
        )

    return OcurrenciaResponse(
        id_ocurrencia=ocurrencia.id_ocurrencia,
        id_especie=ocurrencia.id_especie,
        salida_id=ocurrencia.salida_id,
        fecha_hora=ocurrencia.fecha_hora,
        coordenadas=ocurrencia.coordenadas,
        altitud=ocurrencia.altitud,
        esfuerzo=ocurrencia.esfuerzo,
        cpue=ocurrencia.cpue,
        longitud_pez=ocurrencia.longitud_pez,
        peso=ocurrencia.peso,
        sexo=ocurrencia.sexo,
        estado_ontogenetico=ocurrencia.estado_ontogenetico,
        estadio_vida=ocurrencia.estadio_vida,
        condicion_reproductiva=ocurrencia.condicion_reproductiva,
        comportamiento=ocurrencia.comportamiento,
        anomalias=ocurrencia.anomalias,
        mortalidad=ocurrencia.mortalidad,
        vouchers=ocurrencia.vouchers,
        nivel_certeza=ocurrencia.nivel_certeza,
        ancho_cauce=ocurrencia.ancho_cauce,
        profundidad_media=ocurrencia.profundidad_media,
        profundidad_maxima=ocurrencia.profundidad_maxima,
        caudal_velocidad=ocurrencia.caudal_velocidad,
        tipo_habitat=ocurrencia.tipo_habitat,
        microhabitat=ocurrencia.microhabitat,
        cobertura_dosel=ocurrencia.cobertura_dosel,
        uso_suelo_ribereno=ocurrencia.uso_suelo_ribereno,
        estabilidad_orillas=ocurrencia.estabilidad_orillas,
        sustrato=ocurrencia.sustrato,
        clima=ocurrencia.clima,
        metodo_captura=ocurrencia.metodo_captura,
        arte_pesca=ocurrencia.arte_pesca,
        codigo_muestreo=ocurrencia.codigo_muestreo,
        datum=ocurrencia.datum,
        observaciones=ocurrencia.observaciones,
        nombre_comun=ocurrencia.especie.nombre_comun if ocurrencia.especie else None,
        nombre_cientifico=ocurrencia.especie.nombre_cientifico if ocurrencia.especie else None,
        familia=ocurrencia.especie.familia if ocurrencia.especie else None,
    )

def update_existing_ocurrencia(
    db: Session,
    ocurrencia_id,
    data: OcurrenciaUpdate,
    current_user: User,
) -> OcurrenciaResponse:
    ocurrencia = get_ocurrencia_by_id(db, ocurrencia_id)

    if not ocurrencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ocurrencia no encontrada.",
        )

    salida = get_salida_by_id(db, ocurrencia.salida_id)
    if not salida or salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar esta ocurrencia.",
        )

    fields = [
        "id_especie",
        "fecha_hora",
        "coordenadas",
        "altitud",
        "esfuerzo",
        "cpue",
        "longitud_pez",
        "peso",
        "sexo",
        "estado_ontogenetico",
        "estadio_vida",
        "condicion_reproductiva",
        "comportamiento",
        "anomalias",
        "mortalidad",
        "vouchers",
        "nivel_certeza",
        "ancho_cauce",
        "profundidad_media",
        "profundidad_maxima",
        "caudal_velocidad",
        "tipo_habitat",
        "microhabitat",
        "cobertura_dosel",
        "uso_suelo_ribereno",
        "estabilidad_orillas",
        "sustrato",
        "clima",
        "metodo_captura",
        "arte_pesca",
        "codigo_muestreo",
        "datum",
        "observaciones",
    ]

    for field in fields:
        value = getattr(data, field)
        if value is not None:
            setattr(ocurrencia, field, value)

    updated = update_ocurrencia(db, ocurrencia)
    return OcurrenciaResponse.model_validate(updated)


def delete_existing_ocurrencia(
    db: Session,
    ocurrencia_id,
    current_user: User,
) -> None:
    ocurrencia = get_ocurrencia_by_id(db, ocurrencia_id)

    if not ocurrencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ocurrencia no encontrada.",
        )

    salida = get_salida_by_id(db, ocurrencia.salida_id)
    if not salida or salida.id_usuario != current_user.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta ocurrencia.",
        )

    medicion = get_medicion_by_ocurrencia_id(db, ocurrencia_id)
    if medicion:
        delete_medicion(db, medicion)

    evidencias = delete_evidencias_by_ocurrencia(db, ocurrencia_id)
    for evidencia in evidencias:
        if evidencia.ruta:
            file_path = BASE_DIR / evidencia.ruta
            if file_path.exists() and file_path.is_file():
                try:
                    os.remove(file_path)
                except OSError:
                    pass

    delete_ocurrencia(db, ocurrencia)