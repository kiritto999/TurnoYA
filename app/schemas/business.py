from pydantic import BaseModel, Field
from app.schemas.common import ORMModel


class BusinessCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    logo_url: str | None = Field(default=None, max_length=255)
    categoria: str | None = Field(default=None, max_length=100)
    horario: str | None = Field(default=None, max_length=150)


class BusinessUpdate(BusinessCreate):
    pass


class BusinessStatus(BaseModel):
    estado: str = Field(pattern="^(activo|suspendido|inactivo)$")


class BusinessResponse(ORMModel):
    id_negocio: int
    id_dueno: int
    nombre: str
    logo_url: str | None
    categoria: str | None
    horario: str | None
    estado: str
