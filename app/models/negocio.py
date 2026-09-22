from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Negocio(Base):
    __tablename__ = "negocio"
    id_negocio: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_dueno: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"))
    nombre: Mapped[str] = mapped_column(String(150))
    logo_url: Mapped[str | None] = mapped_column(String(255))
    categoria: Mapped[str | None] = mapped_column(String(100))
    horario: Mapped[str | None] = mapped_column(String(150))
    estado: Mapped[str] = mapped_column(String(20), default="activo")
    dueno: Mapped["Usuario"] = relationship(back_populates="negocios")
    sectores: Mapped[list["Sector"]] = relationship(back_populates="negocio", cascade="all, delete-orphan")
    catalogo: Mapped[list["CatalogoItem"]] = relationship(back_populates="negocio", cascade="all, delete-orphan")
    empleados: Mapped[list["EmpleadoNegocio"]] = relationship(back_populates="negocio", cascade="all, delete-orphan")
