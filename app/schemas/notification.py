from datetime import datetime
from pydantic import BaseModel
from app.schemas.common import ORMModel


class NotificationResponse(ORMModel):
    id_notificacion: int
    id_usuario: int
    id_turno: int | None
    id_negocio: int | None
    tipo: str
    mensaje: str
    leido: bool
    fecha_envio: datetime
