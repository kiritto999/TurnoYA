from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.schemas.common import ORMModel


class RegisterRequest(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    rol: str = Field(pattern="^(cliente|dueño)$")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(ORMModel):
    id_usuario: int
    nombre: str
    email: EmailStr
    rol: str
    estado: str
    fecha_registro: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
