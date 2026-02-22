from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/workspace/watchlist", tags=["workspace-watchlist"])


@router.get("")
async def list_watchlist_items(
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> list[dict]:
    repository = QualityHubRepository(session)
    rows = await repository.list_watchlist_items(current_user.id)
    return [
        {
            "id": row.id,
            "visibility": row.visibility,
            "team_id": row.team_id,
            "project_id": row.project_id,
        }
        for row in rows
    ]
