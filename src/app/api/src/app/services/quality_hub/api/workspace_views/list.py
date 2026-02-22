from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/workspace/views", tags=["workspace-views"])


@router.get("")
async def list_workspace_views(
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> list[dict]:
    repository = QualityHubRepository(session)
    rows = await repository.list_workspace_views(current_user.id)
    return [
        {
            "id": row.id,
            "name": row.name,
            "visibility": row.visibility,
            "team_id": row.team_id,
            "definition_json": row.definition_json,
        }
        for row in rows
    ]
