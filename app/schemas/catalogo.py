from decimal import Decimal
from pydantic import BaseModel, Field
from app.schemas.common import ORMModel


class CatalogItemCreate(BaseModel):
    id_sector: int | None = None
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: str | None = Field(default=None, max_length=255)
    precio: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    tiempo_estimado: int | None = Field(default=None, ge=0)


class CatalogItemResponse(ORMModel):
    id_item: int
    id_negocio: int
    id_sector: int | None
    nombre: str
    descripcion: str | None
    precio: Decimal | None
    tiempo_estimado: int | None
    estado: str
