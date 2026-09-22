from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.models import EmpleadoNegocio, Sector, Usuario
from app.services.business_service import BusinessService
import jwt
from app.core.config import settings


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
        self.business = BusinessService(db)

    def invite(self, business_id: int, user: Usuario, email: str, sector_id: int | None, permisos: str | None):
        self.business.ensure_owner_or_admin(business_id, user)
        invited = self.db.scalar(select(Usuario).where(Usuario.email == email))
        if not invited:
            raise HTTPException(status_code=404, detail="El empleado debe tener un usuario registrado antes de ser invitado")
        if sector_id is not None:
            self.business.ensure_sector(business_id, sector_id)
        existing = self.db.scalar(select(EmpleadoNegocio).where(
            EmpleadoNegocio.id_usuario == invited.id_usuario,
            EmpleadoNegocio.id_negocio == business_id,
        ))
        if existing:
            raise HTTPException(status_code=409, detail="El usuario ya tiene una invitación o pertenencia en este negocio")
        membership = EmpleadoNegocio(
            id_usuario=invited.id_usuario,
            id_negocio=business_id,
            id_sector=sector_id,
            permisos=permisos,
            estado_invitacion="pendiente",
        )
        self.db.add(membership)
        self.db.commit()
        self.db.refresh(membership)
        invitation_token = jwt.encode({"employee_membership": membership.id_empleado_negocio, "uid": invited.id_usuario}, settings.secret_key, algorithm="HS256")
        return membership, invitation_token

    def list(self, business_id: int, user: Usuario):
        self.business.ensure_staff(business_id, user)
        rows = self.db.execute(
            select(EmpleadoNegocio, Usuario.nombre, Usuario.email)
            .join(Usuario, Usuario.id_usuario == EmpleadoNegocio.id_usuario)
            .where(EmpleadoNegocio.id_negocio == business_id)
            .order_by(EmpleadoNegocio.fecha_invitacion.desc())
        ).all()
        return [(row[0], row[1], row[2]) for row in rows]

    def accept(self, token: str, current_user: Usuario):
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            membership_id = int(payload["employee_membership"])
            invited_user_id = int(payload["uid"])
        except (jwt.PyJWTError, KeyError, TypeError, ValueError):
            raise HTTPException(status_code=400, detail="Código de invitación inválido")
        if invited_user_id != current_user.id_usuario:
            raise HTTPException(status_code=403, detail="La invitación no pertenece al usuario autenticado")
        membership = self.db.get(EmpleadoNegocio, membership_id)
        if not membership:
            raise HTTPException(status_code=404, detail="Invitación no encontrada")
        membership.estado_invitacion = "aceptada"
        current_user.rol = "empleado" if current_user.rol == "cliente" else current_user.rol
        self.db.commit()
        self.db.refresh(membership)
        return membership

    def permissions(self, membership_id: int, user: Usuario, permisos: str, sector_id: int | None):
        membership = self.db.get(EmpleadoNegocio, membership_id)
        if not membership:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        self.business.ensure_owner_or_admin(membership.id_negocio, user)
        if sector_id is not None:
            self.business.ensure_sector(membership.id_negocio, sector_id)
        membership.permisos = permisos
        membership.id_sector = sector_id
        self.db.commit()
        self.db.refresh(membership)
        return membership
