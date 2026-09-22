from io import BytesIO
import secrets
import qrcode
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models import CodigoQR, Sector, Usuario
from app.services.business_service import BusinessService


class QRService:
    def __init__(self, db: Session):
        self.db = db
        self.business = BusinessService(db)

    def create(self, business_id: int, user: Usuario, sector_id: int | None):
        self.business.ensure_owner_or_admin(business_id, user)
        if sector_id is not None:
            self.business.ensure_sector(business_id, sector_id)
        code = secrets.token_urlsafe(32)
        destination = f"{settings.frontend_url}/negocios/{business_id}"
        if sector_id:
            destination += f"?sector={sector_id}"
        qr = CodigoQR(id_negocio=business_id, id_sector=sector_id, codigo_unico=code, url_destino=destination)
        self.db.add(qr)
        self.db.commit()
        self.db.refresh(qr)
        return qr

    def list(self, business_id: int, user: Usuario):
        self.business.ensure_owner_or_admin(business_id, user)
        return list(self.db.scalars(select(CodigoQR).where(CodigoQR.id_negocio == business_id).order_by(CodigoQR.fecha_generacion.desc())))

    def resolve(self, code: str):
        qr = self.db.scalar(select(CodigoQR).where(CodigoQR.codigo_unico == code))
        if not qr:
            raise HTTPException(status_code=404, detail="Código QR no encontrado")
        return qr

    def image(self, code: str) -> BytesIO:
        qr = self.resolve(code)
        img = qrcode.make(qr.url_destino)
        stream = BytesIO()
        img.save(stream, format="PNG")
        stream.seek(0)
        return stream
