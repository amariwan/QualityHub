from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.domain.validators import ensure_visibility
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.watchlist import WatchlistUpdateRequest

router = APIRouter(prefix="/workspace/watchlist", tags=["workspace-watchlist"])


@router.put("/{item_id}")
async def update_watchlist_item(
    item_id: int,
    payload: WatchlistUpdateRequest,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    update_payload = payload.model_dump(exclude_none=True)
    if "visibility" in update_payload:
        update_payload["visibility"] = ensure_visibility(update_payload["visibility"])

    repository = QualityHubRepository(session)
    row = await repository.update_watchlist_item(item_id, current_user.id, update_payload)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist item not found")

    return {
        "id": row.id,
        "visibility": row.visibility,
        "team_id": row.team_id,
        "project_id": row.project_id,
    }
