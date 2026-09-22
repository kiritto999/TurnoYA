from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base


class CodigoQR(Base):
    __tablename__ = "codigo_qr"
    id_qr: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_negocio: Mapped[int] = mapped_column(ForeignKey("negocio.id_negocio"))
    id_sector: Mapped[int | None] = mapped_column(ForeignKey("sector.id_sector"))
    codigo_unico: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    url_destino: Mapped[str] = mapped_column(String(255))
    fecha_generacion: Mapped[datetime] = mapped_column(DateTime, default=func.now())
