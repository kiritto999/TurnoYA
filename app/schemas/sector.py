from pydantic import BaseModel, Field
from app.schemas.common import ORMModel


class SectorCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)


class SectorResponse(ORMModel):
    id_sector: int
    id_negocio: int
    nombre: str
    descripcion: str | None
