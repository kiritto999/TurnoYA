from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Sector(Base):
    __tablename__ = "sector"
    id_sector: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_negocio: Mapped[int] = mapped_column(ForeignKey("negocio.id_negocio"))
    nombre: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(String(255))
    negocio: Mapped["Negocio"] = relationship(back_populates="sectores")
