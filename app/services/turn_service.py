from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import CatalogoItem, Sector, Turno, Usuario
from app.repositories.turno_repository import TurnRepository
from app.services.business_service import BusinessService
from app.services.notification_service import NotificationService


class TurnService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TurnRepository(db)
        self.business = BusinessService(db)
        self.notifications = NotificationService(db)

    def create(self, business_id: int, client: Usuario, data):
        business = self.business.ensure_exists(business_id)
        if business.estado != "activo":
            raise HTTPException(status_code=409, detail="El negocio no está disponible")
        if data.id_sector is not None:
            self.business.ensure_sector(business_id, data.id_sector)
        if data.id_item is not None:
            item = self.db.get(CatalogoItem, data.id_item)
            if not item or item.id_negocio != business_id or item.estado != "activo":
                raise HTTPException(status_code=400, detail="Ítem de catálogo inválido")
        number = self.repo.next_number(business_id, data.id_sector)
        try:
            turn = Turno(
                id_cliente=client.id_usuario,
                id_negocio=business_id,
                id_sector=data.id_sector,
                id_item=data.id_item,
                numero_turno=number,
                motivo=data.motivo,
                estado="pendiente",
                fecha_solicitud=datetime.utcnow(),
            )
            self.db.add(turn)
            self.db.flush()
            self.notifications.notify_new_turn(business, turn.id_turno, turn.numero_turno)
            self.db.commit()
            self.db.refresh(turn)
            return turn
        except Exception:
            self.db.rollback()
            raise
        finally:
            self.repo.release_lock()

    def get(self, turn_id: int, user: Usuario):
        turn = self.db.get(Turno, turn_id)
        if not turn:
            raise HTTPException(status_code=404, detail="Turno no encontrado")
        allowed = turn.id_cliente == user.id_usuario
        if user.rol == "superadmin":
            allowed = True
        if user.rol in ("dueño", "empleado"):
            self.business.ensure_staff(turn.id_negocio, user)
            allowed = True
        if not allowed:
            raise HTTPException(status_code=403, detail="No tiene acceso a este turno")
        return turn

    def queue(self, business_id: int, user: Usuario, sector_id: int | None):
        self.business.ensure_staff(business_id, user) if user.rol != "cliente" else self.business.ensure_exists(business_id)
        return self.repo.queue(business_id, sector_id)

    def my_turns(self, user_id: int):
        return self.repo.customer_turns(user_id)

    def change_status(self, turn_id: int, user: Usuario, estado: str):
        turn = self.get(turn_id, user)
        if user.rol == "cliente":
            if turn.id_cliente != user.id_usuario or estado != "cancelado":
                raise HTTPException(status_code=403, detail="El cliente solo puede cancelar su propio turno")
        turn.estado = estado
        if estado == "atendido":
            turn.fecha_atencion = datetime.utcnow()
        self.notifications.notify_turn_change(turn.id_cliente, turn.id_negocio, turn.id_turno, estado)
        self.db.commit()
        self.db.refresh(turn)
        return turn
