from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.domain.validators import ensure_visibility
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.workspace_views import WorkspaceViewUpdateRequest

router = APIRouter(prefix="/workspace/views", tags=["workspace-views"])


@router.put("/{item_id}")
async def update_workspace_view(
    item_id: int,
    payload: WorkspaceViewUpdateRequest,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    update_payload = payload.model_dump(exclude_none=True)
    if "visibility" in update_payload:
        update_payload["visibility"] = ensure_visibility(update_payload["visibility"])

    repository = QualityHubRepository(session)
    row = await repository.update_workspace_view(item_id, current_user.id, update_payload)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace view not found")
    return {
        "id": row.id,
        "name": row.name,
        "visibility": row.visibility,
        "team_id": row.team_id,
        "definition_json": row.definition_json,
    }
