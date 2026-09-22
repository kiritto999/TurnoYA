from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models import Usuario
from app.schemas.catalogo import CatalogItemCreate, CatalogItemResponse
from app.services.catalog_service import CatalogService

router = APIRouter(tags=["Catálogo"])


@router.post("/businesses/{business_id}/catalog", response_model=CatalogItemResponse, status_code=201)
def create_item(business_id: int, data: CatalogItemCreate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return CatalogService(db).create(business_id, user, data)


@router.get("/businesses/{business_id}/catalog", response_model=list[CatalogItemResponse])
def list_items(business_id: int, include_inactive: bool = Query(False), db: Session = Depends(get_db)):
    return CatalogService(db).list(business_id, include_inactive)


@router.get("/catalog/{item_id}", response_model=CatalogItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return CatalogService(db).get(item_id)


@router.put("/catalog/{item_id}", response_model=CatalogItemResponse)
def update_item(item_id: int, data: CatalogItemCreate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return CatalogService(db).update(item_id, user, data)


@router.delete("/catalog/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    CatalogService(db).delete(item_id, user)
