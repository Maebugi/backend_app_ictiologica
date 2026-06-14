import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class SalidaEvidencia(Base):
    __tablename__ = "salida_evidencia"

    id_foto: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )

    salida_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "salidas.salida_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    ruta: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    tipo_archivo: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    observaciones: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    salida = relationship("Salida")