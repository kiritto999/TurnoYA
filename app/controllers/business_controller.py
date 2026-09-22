from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models import Usuario
from app.schemas.business import BusinessCreate, BusinessResponse, BusinessStatus, BusinessUpdate
from app.services.business_service import BusinessService

router = APIRouter(prefix="/businesses", tags=["Negocios"])


@router.post("", response_model=BusinessResponse, status_code=201)
def create_business(data: BusinessCreate, db: Session = Depends(get_db), user: Usuario = Depends(require_roles("dueño"))):
    return BusinessService(db).create(user, data)


@router.get("", response_model=list[BusinessResponse])
def list_businesses(
    nombre: str | None = Query(None),
    categoria: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return BusinessService(db).repo.list_active(nombre, categoria)


@router.get("/admin/all", response_model=list[BusinessResponse])
def all_businesses(db: Session = Depends(get_db), user: Usuario = Depends(require_roles("superadmin"))):
    return BusinessService(db).repo.list_all()


@router.get("/{business_id}", response_model=BusinessResponse)
def get_business(business_id: int, db: Session = Depends(get_db)):
    return BusinessService(db).ensure_exists(business_id)


@router.put("/{business_id}", response_model=BusinessResponse)
def update_business(business_id: int, data: BusinessUpdate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return BusinessService(db).update(business_id, user, data)


@router.patch("/{business_id}/status", response_model=BusinessResponse)
def set_business_status(business_id: int, data: BusinessStatus, db: Session = Depends(get_db), user: Usuario = Depends(require_roles("superadmin"))):
    return BusinessService(db).set_status(business_id, data.estado)
