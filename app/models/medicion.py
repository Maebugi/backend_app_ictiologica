import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Medicion(Base):
    __tablename__ = "mediciones"

    medicion_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    ocurrencia_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ocurrencias.id_ocurrencia", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    oxigeno_disuelto_mg_l: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    ph: Mapped[Decimal | None] = mapped_column(Numeric(4, 2), nullable=True)
    turbidez_ntu: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    conductividad_us_cm: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    tds_mg_l: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    temperatura_c: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    transparencia_secchi_cm: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    nivel_estado_agua: Mapped[str | None] = mapped_column(String(50), nullable=True)
    orp_mv: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    alcalinidad_mg_l: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    dureza_mg_l: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    salinidad: Mapped[Decimal | None] = mapped_column(Numeric(8, 2), nullable=True)
    amonio_mg_l: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    fosforo_metales_mg_l: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    nitratos_mg_l: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    nitritos_mg_l: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    fosfatos_mg_l: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    clorofila_a_ug_l: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    sst_mg_l: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    coliformes_fecales_ufc: Mapped[int | None] = mapped_column(Integer, nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

    ocurrencia = relationship("Ocurrencia")