from pathlib import Path
import shutil
import zipfile

from openpyxl import Workbook
from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories.salida_repository import (
    get_salidas_by_user,
)

from app.repositories.ocurrencia_repository import (
    get_ocurrencias_by_salida,
)

from app.repositories.medicion_repository import (
    get_medicion_by_ocurrencia_id,
)

from app.repositories.evidencia_repository import (
    get_evidencias_by_ocurrencia,
)

from app.repositories.salida_evidencia import (
    get_evidencias_by_salida,
)

from app.repositories.especie_repository import (
    get_species_by_id,
)

from app.repositories.estacion_repository import (
    get_estacion_by_id,
)

def exportar_datos_service(
    db: Session,
    current_user: User,
):
    """
    Servicio principal encargado de exportar toda la
    información ictiológica del usuario.
    """

    # Crear la estructura de exportación
    export_dir = _crear_directorio_exportacion()

    # Obtener toda la información
    datos = _obtener_datos(
        db,
        current_user,
    )

    # Crear el Excel
    _crear_excel(
        export_dir,
        datos,
    )

    # Próximamente
    _copiar_evidencias(
         export_dir,
         datos,
     )

    zip_path = _comprimir_exportacion(
    export_dir,
    )

    return zip_path


def _crear_hoja_ocurrencias(
    wb: Workbook,
    datos: dict,
) -> None:

    ws = wb.create_sheet(
        title="Ocurrencias",
    )
    ws.append([
        "Proyecto",
        "Lugar",
        "Fecha/Hora",
        "Código estación",
        "Nombre estación",
        "Nombre científico",
        "Nombre común",
        "Latitud",
        "Longitud",
        "Altitud",
        "Longitud pez",
        "Peso",
        "Sexo",
        "Estado ontogenético",
        "Estadio vida",
        "Condición reproductiva",
        "Comportamiento",
        "Método captura",
        "Arte pesca",
        "Tipo hábitat",
        "Microhábitat",
        "Clima",
        "Observaciones",
    ])

    for item in datos["ocurrencias"]:

        salida = item["salida"]
        ocurrencia = item["ocurrencia"]
        especie = item["especie"]
        estacion = item["estacion"]

        ws.append([
            salida.nombre_proyecto,
            salida.nombre_lugar,
            ocurrencia.fecha_hora.strftime("%Y-%m-%d %H:%M")
                if ocurrencia.fecha_hora else "",
            estacion.codigo if estacion else "",
            estacion.nombre if estacion else "",
            especie.nombre_cientifico if especie else "",
            especie.nombre_comun if especie else "",
            ocurrencia.latitud,
            ocurrencia.longitud,
            ocurrencia.altitud,
            ocurrencia.longitud_pez,
            ocurrencia.peso,
            ocurrencia.sexo,
            ocurrencia.estado_ontogenetico,
            ocurrencia.estadio_vida,
            ocurrencia.condicion_reproductiva,
            ocurrencia.comportamiento,
            ocurrencia.metodo_captura,
            ocurrencia.arte_pesca,
            ocurrencia.tipo_habitat,
            ocurrencia.microhabitat,
            ocurrencia.clima,
            ocurrencia.observaciones,
        ])

def _crear_hoja_mediciones(
    wb: Workbook,
    datos: dict,
) -> None:

    ws = wb.create_sheet(
        title="Mediciones",
    )

    ws.append([
        "Proyecto",
        "Fecha",
        "Oxígeno disuelto",
        "pH",
        "Temperatura",
        "Conductividad",
        "TDS",
        "Turbidez",
        "Salinidad",
        "ORP",
        "Alcalinidad",
        "Dureza",
        "Nitratos",
        "Nitritos",
        "Fosfatos",
        "Clorofila A",
        "SST",
        "Coliformes",
        "Observaciones",
    ])

    for item in datos["ocurrencias"]:

        medicion = item["medicion"]

        if medicion is None:
            continue

        salida = item["salida"]
        ocurrencia = item["ocurrencia"]

        ws.append([
            salida.nombre_proyecto,
            ocurrencia.fecha_hora.strftime("%Y-%m-%d %H:%M")
                if ocurrencia.fecha_hora else "",

            medicion.oxigeno_disuelto_mg_l,
            medicion.ph,
            medicion.temperatura_c,
            medicion.conductividad_us_cm,
            medicion.tds_mg_l,
            medicion.turbidez_ntu,
            medicion.salinidad,
            medicion.orp_mv,
            medicion.alcalinidad_mg_l,
            medicion.dureza_mg_l,
            medicion.nitratos_mg_l,
            medicion.nitritos_mg_l,
            medicion.fosfatos_mg_l,
            medicion.clorofila_a_ug_l,
            medicion.sst_mg_l,
            medicion.coliformes_fecales_ufc,
            medicion.observaciones,
        ])


def _crear_hoja_evidencias_ocurrencias(
    wb: Workbook,
    datos: dict,
) -> None:
    """
    Crea la hoja con las evidencias asociadas
    a cada ocurrencia.
    """

    ws = wb.create_sheet(
        title="Evidencias Ocurrencias",
    )

    ws.append([
        "Proyecto",
        "Lugar",
        "Código estación",
        "Nombre científico",
        "Nombre común",
        "Ruta archivo",
        "Observaciones",
    ])

    for item in datos["ocurrencias"]:

        salida = item["salida"]
        especie = item["especie"]
        estacion = item["estacion"]
        ocurrencia = item["ocurrencia"]

        evidencias = [
            e
            for e in datos["evidencias_ocurrencias"]
            if e.id_ocurrencia == ocurrencia.id_ocurrencia
        ]

        for evidencia in evidencias:

            ws.append([
                salida.nombre_proyecto,
                salida.nombre_lugar,
                estacion.codigo if estacion else "",
                especie.nombre_cientifico if especie else "",
                especie.nombre_comun if especie else "",
                evidencia.ruta,
                evidencia.observaciones,
            ])


def _crear_hoja_evidencias_salidas(
    wb: Workbook,
    datos: dict,
) -> None:
    """
    Crea la hoja de evidencias asociadas
    directamente a las salidas.
    """

    ws = wb.create_sheet(
        title="Evidencias Salidas",
    )

    ws.append([
        "Proyecto",
        "Lugar",
        "Ruta archivo",
        "Tipo archivo",
        "Observaciones",
    ])

    for salida in datos["salidas"]:

        evidencias = [
            e
            for e in datos["evidencias_salidas"]
            if e.salida_id == salida.salida_id
        ]

        for evidencia in evidencias:

            ws.append([
                salida.nombre_proyecto,
                salida.nombre_lugar,
                evidencia.ruta,
                evidencia.tipo_archivo,
                evidencia.observaciones,
            ])


def _crear_excel(
    export_dir: Path,
    datos: dict,
)-> None:
    """
    Crea el archivo Excel principal.
    """

    wb = Workbook()

    _crear_hoja_salidas(
        wb,
        datos,
    )

    _crear_hoja_ocurrencias(
        wb,
        datos,
    )

    _crear_hoja_mediciones(
        wb,
        datos,
    )

    _crear_hoja_evidencias_ocurrencias(
        wb,
        datos,
    )
    _crear_hoja_evidencias_salidas(
        wb,
        datos,
)

    # Próximamente
    # _crear_hoja_ocurrencias(wb, datos)
    # _crear_hoja_mediciones(wb, datos)
    # _crear_hoja_estaciones(wb, datos)
    # _crear_hoja_evidencias_ocurrencias(wb, datos)
    # _crear_hoja_evidencias_salidas(wb, datos)


    archivo_excel = export_dir / "informacion_ictiologica.xlsx"

    wb.save(archivo_excel)



def _crear_hoja_salidas(
    wb: Workbook,
    datos: dict,
)-> None:
    """
    Crea la hoja de Salidas.
    """

    ws = wb.active

    ws.title = "Salidas"

    ws.append([
        "Proyecto",
        "Lugar",
        "Fecha inicio",
        "Fecha fin",
        "Estado",
        "Observaciones",
    ])

    for salida in datos["salidas"]:

        ws.append([
            salida.nombre_proyecto,
            salida.nombre_lugar,
            salida.fecha_inicio.strftime("%Y-%m-%d %H:%M")
                if salida.fecha_inicio else "",

            salida.fecha_fin.strftime("%Y-%m-%d %H:%M")
                if salida.fecha_fin else "",
            salida.estado,
            salida.observaciones,
        ])



def _copiar_evidencias(
    export_dir: Path,
    datos: dict,
) -> None:
    """
    Crea la estructura de carpetas donde posteriormente
    se copiarán todas las evidencias.
    """

    base_dir = Path(__file__).resolve().parents[2]

    evidencias_dir = export_dir / "Evidencias"

    for salida in datos["salidas"]:

        nombre_proyecto = (
            salida.nombre_proyecto
            if salida.nombre_proyecto
            else "Proyecto_Sin_Nombre"
        )

        proyecto_dir = evidencias_dir / nombre_proyecto

        salida_dir = proyecto_dir / "Salida"

        ocurrencias_dir = proyecto_dir / "Ocurrencias"

        salida_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        ocurrencias_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        evidencias_salida = [
            e
            for e in datos["evidencias_salidas"]
            if e.salida_id == salida.salida_id
        ]

        for evidencia in evidencias_salida:

            if not evidencia.ruta:
                continue

            origen = base_dir / evidencia.ruta

            destino = (
                salida_dir /
                Path(evidencia.ruta).name
            )

            if origen.exists():

                shutil.copy2(
                    origen,
                    destino,
                )
            else:

                print(
                    f"No existe el archivo: {origen}"
                )

            # Crear una carpeta por cada ocurrencia
        ocurrencias_proyecto = [
            item
            for item in datos["ocurrencias"]
            if item["salida"].salida_id == salida.salida_id
        ]

        for item in ocurrencias_proyecto:

            ocurrencia = item["ocurrencia"]

            codigo = (
                ocurrencia.codigo_muestreo
                if ocurrencia.codigo_muestreo
                else str(ocurrencia.id_ocurrencia)
            )

            carpeta_ocurrencia = (
                ocurrencias_dir / codigo
            )

            carpeta_ocurrencia.mkdir(
                
                exist_ok=True,    
            )

            evidencias_ocurrencia = [
                e
                for e in datos["evidencias_ocurrencias"]
                if e.id_ocurrencia == ocurrencia.id_ocurrencia
            ]

            for evidencia in evidencias_ocurrencia:

                if not evidencia.ruta:
                    continue

                origen = base_dir / evidencia.ruta

                destino = (
                    carpeta_ocurrencia /
                    Path(evidencia.ruta).name
                )

                if origen.exists():

                    shutil.copy2(
                        origen,
                        destino,
                    )
                else:

                    print(
                        f"No existe el archivo: {origen}"
                    )


def _comprimir_exportacion(
    export_dir: Path,
) -> Path:
    """
    Comprime toda la carpeta de exportación en un ZIP.
    """

    zip_path = export_dir.with_suffix(".zip")

    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED,
    ) as zipf:

        for archivo in export_dir.rglob("*"):

            zipf.write(
                archivo,
                archivo.relative_to(
                    export_dir.parent,
                ),
            )

    return zip_path


def _crear_directorio_exportacion() -> Path:
    """
    Crea la estructura base donde se generará
    toda la exportación.
    """

    base_dir = Path(__file__).resolve().parents[2]

    export_dir = base_dir / "Exportacion_Ictiologica"

    if export_dir.exists():
        shutil.rmtree(export_dir)

    export_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    (export_dir / "Evidencias").mkdir()

    return export_dir


def _obtener_datos(
    db: Session,
    current_user: User,
) -> dict:
    """
    Consulta toda la información necesaria
    para la exportación.
    """

    salidas = get_salidas_by_user(
        db,
        current_user.usuario_id,
    )

    ocurrencias = []
    mediciones = []
    evidencias_ocurrencias = []
    evidencias_salidas = []

    for salida in salidas:

        # Evidencias de la salida
        evidencias_salidas.extend(
            get_evidencias_by_salida(
                db,
                salida.salida_id,
            )
        )

        # Ocurrencias de la salida
        lista_ocurrencias = get_ocurrencias_by_salida(
            db,
            salida.salida_id,
        )

        for ocurrencia in lista_ocurrencias:

            especie = get_species_by_id(
                db,
                ocurrencia.id_especie,
            )

            estacion = get_estacion_by_id(
                db,
                ocurrencia.estacion_id,
            )

            medicion = get_medicion_by_ocurrencia_id(
                db,
                ocurrencia.id_ocurrencia,
            )

            if medicion:
                mediciones.append(medicion)

            evidencias_ocurrencias.extend(
                get_evidencias_by_ocurrencia(
                    db,
                    ocurrencia.id_ocurrencia,
                )
            )

            ocurrencias.append(
                {
                    "ocurrencia": ocurrencia,
                    "salida": salida,
                    "especie": especie,
                    "estacion": estacion,
                    "medicion": medicion,
                }
            )

    return {
        "usuario": current_user,
        "salidas": salidas,
        "ocurrencias": ocurrencias,
        "mediciones": mediciones,
        "evidencias_ocurrencias": evidencias_ocurrencias,
        "evidencias_salidas": evidencias_salidas,
    } 