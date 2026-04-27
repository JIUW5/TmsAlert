from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.v1.alerts import router as alerts_router

router = APIRouter()
router.include_router(health_router, tags=['health'])
router.include_router(alerts_router, prefix='/v1', tags=['alerts'])
