from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class CatalogoItem(Base):
    __tablename__ = "catalogo_item"
    id_item: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_negocio: Mapped[int] = mapped_column(ForeignKey("negocio.id_negocio"))
    id_sector: Mapped[int | None] = mapped_column(ForeignKey("sector.id_sector"))
    nombre: Mapped[str] = mapped_column(String(150))
    descripcion: Mapped[str | None] = mapped_column(String(255))
    precio: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    tiempo_estimado: Mapped[int | None]
    estado: Mapped[str] = mapped_column(String(20), default="activo")
    negocio: Mapped["Negocio"] = relationship(back_populates="catalogo")
