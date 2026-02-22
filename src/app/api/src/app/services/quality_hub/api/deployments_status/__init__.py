from __future__ import annotations

from fastapi import APIRouter

from app.services.quality_hub.api.deployments_status.get import router as get_router
from app.services.quality_hub.api.deployments_status.list import router as list_router

router = APIRouter()
router.include_router(list_router)
router.include_router(get_router)
