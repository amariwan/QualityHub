from __future__ import annotations

from fastapi import APIRouter

from app.services.quality_hub.api import router as quality_hub_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(quality_hub_router)
