from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Notificacion


class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: int):
        return list(self.db.scalars(select(Notificacion).where(Notificacion.id_usuario == user_id).order_by(Notificacion.fecha_envio.desc())))

    def get(self, notification_id: int):
        return self.db.get(Notificacion, notification_id)
