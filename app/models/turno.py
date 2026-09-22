from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Turno(Base):
    __tablename__ = "turno"
    id_turno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    id_negocio: Mapped[int] = mapped_column(ForeignKey("negocio.id_negocio"))
    id_sector: Mapped[int | None] = mapped_column(ForeignKey("sector.id_sector"))
    id_item: Mapped[int | None] = mapped_column(ForeignKey("catalogo_item.id_item"))
    numero_turno: Mapped[int]
    motivo: Mapped[str | None] = mapped_column(String(255))
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")
    fecha_solicitud: Mapped[datetime] = mapped_column(DateTime)
    fecha_atencion: Mapped[datetime | None] = mapped_column(DateTime)
