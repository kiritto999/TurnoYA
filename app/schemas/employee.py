from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.schemas.common import ORMModel


class EmployeeInviteCreate(BaseModel):
    email: EmailStr
    id_sector: int | None = None
    permisos: str | None = Field(default=None, max_length=255)


class EmployeeResponse(ORMModel):
    id_empleado_negocio: int
    id_usuario: int
    id_negocio: int
    id_sector: int | None
    permisos: str | None
    estado_invitacion: str
    fecha_invitacion: datetime
    email: EmailStr | None = None
    nombre: str | None = None


class EmployeePermissionsUpdate(BaseModel):
    permisos: str = Field(max_length=255)
    id_sector: int | None = None
