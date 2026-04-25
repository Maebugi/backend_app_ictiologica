import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Ocurrencia(Base):
    __tablename__ = "ocurrencias"

    id_ocurrencia: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    id_especie: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("especies.especie_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    salida_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("salidas.salida_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )

    fecha_hora: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    coordenadas: Mapped[str | None] = mapped_column(String(50), nullable=True)
    altitud: Mapped[float | None] = mapped_column(Float, nullable=True)
    esfuerzo: Mapped[float | None] = mapped_column(Float, nullable=True)
    cpue: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitud_pez: Mapped[float | None] = mapped_column(Float, nullable=True)
    peso: Mapped[float | None] = mapped_column(Float, nullable=True)
    sexo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    estado_ontogenetico: Mapped[str | None] = mapped_column(String(30), nullable=True)
    estadio_vida: Mapped[str | None] = mapped_column(String(30), nullable=True)
    condicion_reproductiva: Mapped[str | None] = mapped_column(String(30), nullable=True)
    comportamiento: Mapped[str | None] = mapped_column(String(50), nullable=True)
    anomalias: Mapped[str | None] = mapped_column(Text, nullable=True)
    mortalidad: Mapped[str | None] = mapped_column(String(30), nullable=True)
    vouchers: Mapped[str | None] = mapped_column(String(100), nullable=True)
    nivel_certeza: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ancho_cauce: Mapped[float | None] = mapped_column(Float, nullable=True)
    profundidad_media: Mapped[float | None] = mapped_column(Float, nullable=True)
    profundidad_maxima: Mapped[float | None] = mapped_column(Float, nullable=True)
    caudal_velocidad: Mapped[float | None] = mapped_column(Float, nullable=True)
    tipo_habitat: Mapped[str | None] = mapped_column(String(50), nullable=True)
    microhabitat: Mapped[str | None] = mapped_column(String(50), nullable=True)
    cobertura_dosel: Mapped[float | None] = mapped_column(Float, nullable=True)
    uso_suelo_ribereno: Mapped[str | None] = mapped_column(String(50), nullable=True)
    estabilidad_orillas: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sustrato: Mapped[str | None] = mapped_column(String(50), nullable=True)
    clima: Mapped[str | None] = mapped_column(String(50), nullable=True)
    metodo_captura: Mapped[str | None] = mapped_column(String(50), nullable=True)
    arte_pesca: Mapped[str | None] = mapped_column(String(50), nullable=True)
    codigo_muestreo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    datum: Mapped[str | None] = mapped_column(String(20), nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

    especie = relationship("Especie")
    salida = relationship("Salida")