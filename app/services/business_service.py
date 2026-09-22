from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import EmpleadoNegocio, Negocio, Sector, Usuario
from app.repositories.business_repository import BusinessRepository


class BusinessService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BusinessRepository(db)

    def ensure_exists(self, business_id: int):
        business = self.repo.get(business_id)
        if not business:
            raise HTTPException(status_code=404, detail="Negocio no encontrado")
        return business

    def ensure_owner_or_admin(self, business_id: int, user: Usuario):
        business = self.ensure_exists(business_id)
        if user.rol not in ("superadmin", "dueño") or (user.rol == "dueño" and business.id_dueno != user.id_usuario):
            raise HTTPException(status_code=403, detail="No tiene acceso administrativo a este negocio")
        return business

    def ensure_staff(self, business_id: int, user: Usuario):
        business = self.ensure_exists(business_id)
        if user.rol == "superadmin":
            return business
        if user.rol == "dueño" and business.id_dueno == user.id_usuario:
            return business
        membership = self.db.scalar(select(EmpleadoNegocio).where(
            EmpleadoNegocio.id_negocio == business_id,
            EmpleadoNegocio.id_usuario == user.id_usuario,
            EmpleadoNegocio.estado_invitacion == "aceptada",
        ))
        if not membership:
            raise HTTPException(status_code=403, detail="El usuario no pertenece al negocio")
        return business

    def ensure_sector(self, business_id: int, sector_id: int):
        sector = self.db.get(Sector, sector_id)
        if not sector or sector.id_negocio != business_id:
            raise HTTPException(status_code=400, detail="Sector inválido para el negocio")
        return sector

    def create(self, user: Usuario, data):
        business = Negocio(id_dueno=user.id_usuario, **data.model_dump())
        self.db.add(business)
        self.db.commit()
        self.db.refresh(business)
        return business

    def update(self, business_id: int, user: Usuario, data):
        business = self.ensure_owner_or_admin(business_id, user)
        for key, value in data.model_dump().items():
            setattr(business, key, value)
        self.db.commit()
        self.db.refresh(business)
        return business

    def set_status(self, business_id: int, estado: str):
        business = self.ensure_exists(business_id)
        business.estado = estado
        self.db.commit()
        self.db.refresh(business)
        return business
