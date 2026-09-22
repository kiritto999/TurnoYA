from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import CatalogoItem, Usuario
from app.services.business_service import BusinessService


class CatalogService:
    def __init__(self, db: Session):
        self.db = db
        self.business = BusinessService(db)

    def create(self, business_id: int, user: Usuario, data):
        self.business.ensure_owner_or_admin(business_id, user)
        if data.id_sector is not None:
            self.business.ensure_sector(business_id, data.id_sector)
        item = CatalogoItem(id_negocio=business_id, **data.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list(self, business_id: int, include_inactive: bool = False):
        self.business.ensure_exists(business_id)
        stmt = select(CatalogoItem).where(CatalogoItem.id_negocio == business_id)
        if not include_inactive:
            stmt = stmt.where(CatalogoItem.estado == "activo")
        return list(self.db.scalars(stmt.order_by(CatalogoItem.nombre)))

    def get(self, item_id: int):
        item = self.db.get(CatalogoItem, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Ítem de catálogo no encontrado")
        return item

    def update(self, item_id: int, user: Usuario, data):
        item = self.get(item_id)
        self.business.ensure_owner_or_admin(item.id_negocio, user)
        if data.id_sector is not None:
            self.business.ensure_sector(item.id_negocio, data.id_sector)
        for key, value in data.model_dump().items():
            setattr(item, key, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int, user: Usuario):
        item = self.get(item_id)
        self.business.ensure_owner_or_admin(item.id_negocio, user)
        item.estado = "inactivo"
        self.db.commit()
