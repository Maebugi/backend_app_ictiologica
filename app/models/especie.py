import uuid

from sqlalchemy import Integer, String, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Especie(Base):
    __tablename__ = "especies"

    especie_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    nombre_cientifico: Mapped[str | None] = mapped_column(String(150), nullable=True)
    nombre_comun: Mapped[str | None] = mapped_column(String(100), nullable=True)
    orden: Mapped[str | None] = mapped_column(String(80), nullable=True)
    familia: Mapped[str | None] = mapped_column(String(80), nullable=True)
    longitud_estandar: Mapped[float | None] = mapped_column(Float, nullable=True)
    talla_maxima: Mapped[float | None] = mapped_column(Float, nullable=True)
    peso_maximo: Mapped[float | None] = mapped_column(Float, nullable=True)
    longevidad: Mapped[int | None] = mapped_column(Integer, nullable=True)
    habito_alimenticio: Mapped[str | None] = mapped_column(String(100), nullable=True)
    reproductivo: Mapped[str | None] = mapped_column(String(100), nullable=True)
    periodo_reproductivo: Mapped[str | None] = mapped_column(String(100), nullable=True)
    estado_conservacion: Mapped[str | None] = mapped_column(String(50), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
