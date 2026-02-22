from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.domain.validators import ensure_visibility
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.tags import TagUpdateRequest

router = APIRouter(prefix="/workspace/tags", tags=["workspace-tags"])


@router.put("/{tag_id}")
async def update_tag(
    tag_id: int,
    payload: TagUpdateRequest,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    update_payload = payload.model_dump(exclude_none=True)
    links = update_payload.pop("links", None)
    if "visibility" in update_payload:
        update_payload["visibility"] = ensure_visibility(update_payload["visibility"])

    repository = QualityHubRepository(session)
    row = await repository.update_tag(tag_id, current_user.id, update_payload)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    if links is not None:
        await repository.replace_tag_links(tag_id, links)

    current_links = await repository.list_tag_links(tag_id)
    return {
        "id": row.id,
        "visibility": row.visibility,
        "team_id": row.team_id,
        "name": row.name,
        "color": row.color,
        "links": [
            {
                "id": link.id,
                "scope_type": link.scope_type,
                "project_id": link.project_id,
                "env": link.env,
                "cluster_id": link.cluster_id,
            }
            for link in current_links
        ],
    }
