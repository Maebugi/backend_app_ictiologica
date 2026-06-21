import uuid

from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Estacion(Base):
    __tablename__ = "estaciones"

    estacion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )

    codigo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    cuerpo_agua: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    latitud: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitud: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )