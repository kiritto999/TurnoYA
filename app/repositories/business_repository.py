from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from app.models import Negocio


class BusinessRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, business_id: int):
        return self.db.get(Negocio, business_id)

    def list_active(self, nombre: str | None = None, categoria: str | None = None):
        stmt = select(Negocio).where(Negocio.estado == "activo")
        if nombre:
            stmt = stmt.where(Negocio.nombre.ilike(f"%{nombre}%"))
        if categoria:
            stmt = stmt.where(Negocio.categoria.ilike(f"%{categoria}%"))
        return list(self.db.scalars(stmt.order_by(Negocio.nombre)))

    def list_all(self):
        return list(self.db.scalars(select(Negocio).order_by(Negocio.nombre)))
