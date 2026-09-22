from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int):
        return self.db.get(Usuario, user_id)

    def get_by_email(self, email: str):
        return self.db.scalar(select(Usuario).where(Usuario.email == email))

    def save(self, user: Usuario):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
