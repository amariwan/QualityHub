from __future__ import annotations

from fastapi import APIRouter

from app.services.quality_hub.api.auth_token.create import router as create_router
from app.services.quality_hub.api.auth_token.delete import router as delete_router
from app.services.quality_hub.api.auth_token.get import router as get_router

router = APIRouter()
router.include_router(create_router)
router.include_router(get_router)
router.include_router(delete_router)
