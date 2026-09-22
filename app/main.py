from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.controllers.auth_controller import router as auth_router
from app.controllers.business_controller import router as business_router
from app.controllers.sector_controller import router as sector_router
from app.controllers.catalog_controller import router as catalog_router
from app.controllers.employee_controller import router as employee_router
from app.controllers.qr_controller import router as qr_router
from app.controllers.turn_controller import router as turn_router
from app.controllers.notification_controller import router as notification_router
from app import models  # noqa: F401 — registra modelos para SQLAlchemy

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API REST de TurnoYa basada en FastAPI, MySQL y arquitectura multicapa.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(business_router, prefix="/api/v1")
app.include_router(sector_router, prefix="/api/v1")
app.include_router(catalog_router, prefix="/api/v1")
app.include_router(employee_router, prefix="/api/v1")
app.include_router(qr_router, prefix="/api/v1")
app.include_router(turn_router, prefix="/api/v1")
app.include_router(notification_router, prefix="/api/v1")


@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok", "service": settings.app_name}
