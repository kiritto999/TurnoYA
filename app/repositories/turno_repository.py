from sqlalchemy import func, select, text
from sqlalchemy.orm import Session
from app.models import Turno


class TurnRepository:
    def __init__(self, db: Session):
        self.db = db

    def next_number(self, business_id: int, sector_id: int | None) -> int:
        lock_name = f"turnoya:turno:{business_id}:{sector_id or 0}"
        locked = self.db.scalar(text("SELECT GET_LOCK(:lock_name, 5)"), {"lock_name": lock_name})
        if locked != 1:
            raise TimeoutError("No se pudo adquirir el bloqueo para generar el número de turno")
        self._lock_name = lock_name
        current = self.db.scalar(
            select(func.coalesce(func.max(Turno.numero_turno), 0)).where(
                Turno.id_negocio == business_id,
                Turno.id_sector == sector_id,
            )
        ) or 0
        return int(current) + 1

    def release_lock(self):
        if getattr(self, "_lock_name", None):
            self.db.execute(text("SELECT RELEASE_LOCK(:lock_name)"), {"lock_name": self._lock_name})
            self._lock_name = None

    def get(self, turn_id: int):
        return self.db.get(Turno, turn_id)

    def queue(self, business_id: int, sector_id: int | None = None):
        stmt = select(Turno).where(
            Turno.id_negocio == business_id,
            Turno.estado.in_(["pendiente", "llamado", "atendiendo"]),
        )
        if sector_id is not None:
            stmt = stmt.where(Turno.id_sector == sector_id)
        return list(self.db.scalars(stmt.order_by(Turno.numero_turno)))

    def customer_turns(self, user_id: int):
        return list(self.db.scalars(select(Turno).where(Turno.id_cliente == user_id).order_by(Turno.fecha_solicitud.desc())))
