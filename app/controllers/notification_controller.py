from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Usuario
from app.schemas.notification import NotificationResponse
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notificaciones"])


@router.get("", response_model=list[NotificationResponse])
def notifications(db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return NotificationService(db).list(user.id_usuario)


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_read(notification_id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return NotificationService(db).mark_read(notification_id, user)
