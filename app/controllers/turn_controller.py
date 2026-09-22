from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models import Usuario
from app.schemas.turno import TurnCreate, TurnResponse, TurnStatusUpdate
from app.services.turn_service import TurnService

router = APIRouter(tags=["Turnos"])


@router.post("/businesses/{business_id}/turns", response_model=TurnResponse, status_code=201)
def create_turn(business_id: int, data: TurnCreate, db: Session = Depends(get_db), user: Usuario = Depends(require_roles("cliente"))):
    return TurnService(db).create(business_id, user, data)


@router.get("/businesses/{business_id}/queue", response_model=list[TurnResponse])
def queue(business_id: int, sector_id: int | None = Query(None), db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return TurnService(db).queue(business_id, user, sector_id)


@router.get("/turns/my", response_model=list[TurnResponse])
def my_turns(db: Session = Depends(get_db), user: Usuario = Depends(require_roles("cliente"))):
    return TurnService(db).my_turns(user.id_usuario)


@router.get("/turns/{turn_id}", response_model=TurnResponse)
def get_turn(turn_id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return TurnService(db).get(turn_id, user)


@router.patch("/turns/{turn_id}/status", response_model=TurnResponse)
def change_status(turn_id: int, data: TurnStatusUpdate, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)):
    return TurnService(db).change_status(turn_id, user, data.estado)
