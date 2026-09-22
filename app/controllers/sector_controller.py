from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Usuario
from app.schemas.sector import SectorCreate, SectorResponse
from app.services.sector_service import SectorService

router = APIRouter(tags=["Sectores"])


@router.post("/businesses/{business_id}/sectors", response_model=SectorResponse, status_code=201)
def create_sector(business_id: int, data: SectorCreate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return SectorService(db).create(business_id, user, data)


@router.get("/businesses/{business_id}/sectors", response_model=list[SectorResponse])
def list_sectors(business_id: int, db: Session = Depends(get_db)):
    return SectorService(db).list(business_id)


@router.get("/sectors/{sector_id}", response_model=SectorResponse)
def get_sector(sector_id: int, db: Session = Depends(get_db)):
    return SectorService(db).get(sector_id)


@router.put("/sectors/{sector_id}", response_model=SectorResponse)
def update_sector(sector_id: int, data: SectorCreate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return SectorService(db).update(sector_id, user, data)


@router.delete("/sectors/{sector_id}", status_code=204)
def delete_sector(sector_id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    SectorService(db).delete(sector_id, user)
