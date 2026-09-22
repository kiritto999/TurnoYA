"""Crea un superadmin en una BD TurnoYa existente."""
import getpass
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import Usuario


def main():
    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip().lower()
    password = getpass.getpass("Contraseña: ")
    db = SessionLocal()
    try:
        if db.query(Usuario).filter(Usuario.email == email).first():
            raise SystemExit("Ese email ya existe.")
        user = Usuario(nombre=nombre, email=email, password_hash=hash_password(password), rol="superadmin", estado="activo")
        db.add(user)
        db.commit()
        print(f"Superadmin creado: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
