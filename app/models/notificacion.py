from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base


class Notificacion(Base):
    __tablename__ = "notificacion"
    id_notificacion: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    id_turno: Mapped[int | None] = mapped_column(ForeignKey("turno.id_turno"))
    id_negocio: Mapped[int | None] = mapped_column(ForeignKey("negocio.id_negocio"))
    tipo: Mapped[str] = mapped_column(String(30))
    mensaje: Mapped[str] = mapped_column(String(255))
    leido: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_envio: Mapped[datetime] = mapped_column(DateTime, default=func.now())
