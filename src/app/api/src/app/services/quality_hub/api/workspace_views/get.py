from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/workspace/views", tags=["workspace-views"])


@router.get("/{item_id}")
async def get_workspace_view(
    item_id: int,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    row = await repository.get_workspace_view(item_id, current_user.id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace view not found")
    return {
        "id": row.id,
        "name": row.name,
        "visibility": row.visibility,
        "team_id": row.team_id,
        "definition_json": row.definition_json,
    }
