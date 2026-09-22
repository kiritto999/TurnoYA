from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Sector, Usuario
from app.services.business_service import BusinessService


class SectorService:
    def __init__(self, db: Session):
        self.db = db
        self.business = BusinessService(db)

    def create(self, business_id: int, user: Usuario, data):
        self.business.ensure_owner_or_admin(business_id, user)
        sector = Sector(id_negocio=business_id, **data.model_dump())
        self.db.add(sector)
        self.db.commit()
        self.db.refresh(sector)
        return sector

    def list(self, business_id: int):
        self.business.ensure_exists(business_id)
        return list(self.db.scalars(select(Sector).where(Sector.id_negocio == business_id).order_by(Sector.nombre)))

    def get(self, sector_id: int):
        sector = self.db.get(Sector, sector_id)
        if not sector:
            raise HTTPException(status_code=404, detail="Sector no encontrado")
        return sector

    def update(self, sector_id: int, user: Usuario, data):
        sector = self.get(sector_id)
        self.business.ensure_owner_or_admin(sector.id_negocio, user)
        for key, value in data.model_dump().items():
            setattr(sector, key, value)
        self.db.commit()
        self.db.refresh(sector)
        return sector

    def delete(self, sector_id: int, user: Usuario):
        sector = self.get(sector_id)
        self.business.ensure_owner_or_admin(sector.id_negocio, user)
        self.db.delete(sector)
        self.db.commit()
