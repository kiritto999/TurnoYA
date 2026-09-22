from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.security import create_access_token, hash_password, verify_password
from app.models import Usuario
from app.repositories.usuario_repository import UsuarioRepository


class AuthService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def register(self, nombre: str, email: str, password: str, rol: str):
        if self.repo.get_by_email(email):
            raise HTTPException(status_code=409, detail="El correo ya está registrado")
        user = Usuario(
            nombre=nombre,
            email=email,
            password_hash=hash_password(password),
            rol=rol,
            estado="activo",
            fecha_registro=datetime.utcnow(),
        )
        try:
            return self.repo.save(user)
        except IntegrityError:
            self.repo.db.rollback()
            raise HTTPException(status_code=409, detail="No fue posible registrar el usuario")

    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user or user.estado != "activo" or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
        return user, create_access_token(user)
