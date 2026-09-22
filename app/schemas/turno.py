from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import ORMModel


class TurnCreate(BaseModel):
    id_sector: int | None = None
    id_item: int | None = None
    motivo: str | None = Field(default=None, max_length=255)


class TurnResponse(ORMModel):
    id_turno: int
    id_cliente: int
    id_negocio: int
    id_sector: int | None
    id_item: int | None
    numero_turno: int
    motivo: str | None
    estado: str
    fecha_solicitud: datetime
    fecha_atencion: datetime | None


class TurnStatusUpdate(BaseModel):
    estado: str = Field(pattern="^(pendiente|llamado|atendiendo|atendido|cancelado|ausente)$")
