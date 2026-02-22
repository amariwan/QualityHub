from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.domain.validators import ensure_visibility
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.workspace_views import WorkspaceViewCreateRequest

router = APIRouter(prefix="/workspace/views", tags=["workspace-views"])


@router.post("")
async def create_workspace_view(
    payload: WorkspaceViewCreateRequest,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    item = await repository.create_workspace_view(
        owner_user_id=current_user.id,
        visibility=ensure_visibility(payload.visibility),
        team_id=payload.team_id,
        name=payload.name,
        definition_json=payload.definition_json,
    )
    return {
        "id": item.id,
        "name": item.name,
        "visibility": item.visibility,
        "team_id": item.team_id,
        "definition_json": item.definition_json,
    }
