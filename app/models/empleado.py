from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base


class EmpleadoNegocio(Base):
    __tablename__ = "empleado_negocio"
    id_empleado_negocio: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    id_negocio: Mapped[int] = mapped_column(ForeignKey("negocio.id_negocio"))
    id_sector: Mapped[int | None] = mapped_column(ForeignKey("sector.id_sector"))
    permisos: Mapped[str | None] = mapped_column(String(255))
    estado_invitacion: Mapped[str] = mapped_column(String(20), default="pendiente")
    fecha_invitacion: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    negocio: Mapped["Negocio"] = relationship(back_populates="empleados")
