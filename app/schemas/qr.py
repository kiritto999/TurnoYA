from datetime import datetime
from pydantic import BaseModel
from app.schemas.common import ORMModel


class QRCreate(BaseModel):
    id_sector: int | None = None


class QRResponse(ORMModel):
    id_qr: int
    id_negocio: int
    id_sector: int | None
    codigo_unico: str
    url_destino: str
    fecha_generacion: datetime
