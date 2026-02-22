from __future__ import annotations

from fastapi import APIRouter

from app.services.quality_hub.api.workspace_watchlist.create import router as create_router
from app.services.quality_hub.api.workspace_watchlist.delete import router as delete_router
from app.services.quality_hub.api.workspace_watchlist.get import router as get_router
from app.services.quality_hub.api.workspace_watchlist.list import router as list_router
from app.services.quality_hub.api.workspace_watchlist.update import router as update_router

router = APIRouter()
router.include_router(create_router)
router.include_router(list_router)
router.include_router(get_router)
router.include_router(update_router)
router.include_router(delete_router)
