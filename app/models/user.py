import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "usuarios"

    usuario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    rol_id: Mapped[int] = mapped_column(
        ForeignKey("roles.rol_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False
    )
    nombre: Mapped[str | None] = mapped_column(String(150), nullable=True)
    correo: Mapped[str | None] = mapped_column(String(150), unique=True, nullable=True)
    contrasena: Mapped[str | None] = mapped_column(String(255), nullable=True)
    institucion: Mapped[str | None] = mapped_column(String(150), nullable=True)
    fecha_registro: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    rol = relationship("Role", back_populates="usuarios")