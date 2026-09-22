from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Usuario
from app.schemas.qr import QRCreate, QRResponse
from app.services.qr_service import QRService

router = APIRouter(tags=["QR"])


@router.post("/businesses/{business_id}/qr", response_model=QRResponse, status_code=201)
def create_qr(business_id: int, data: QRCreate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return QRService(db).create(business_id, user, data.id_sector)


@router.get("/businesses/{business_id}/qr", response_model=list[QRResponse])
def list_qr(business_id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return QRService(db).list(business_id, user)


@router.get("/qr/{code}", response_model=QRResponse)
def resolve_qr(code: str, db: Session = Depends(get_db)):
    return QRService(db).resolve(code)


@router.get("/qr/{code}/image")
def qr_image(code: str, db: Session = Depends(get_db)):
    stream = QRService(db).image(code)
    return StreamingResponse(stream, media_type="image/png", headers={"Content-Disposition": f"inline; filename=turnoya-{code}.png"})
