import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EvidenciaOcurrencia(Base):
    __tablename__ = "evidencia_ocurrencia"

    id_foto: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    id_ocurrencia: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ocurrencias.id_ocurrencia", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    ruta: Mapped[str | None] = mapped_column(String(255), nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

    ocurrencia = relationship("Ocurrencia")