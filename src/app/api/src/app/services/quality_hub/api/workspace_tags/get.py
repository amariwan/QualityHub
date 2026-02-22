from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/workspace/tags", tags=["workspace-tags"])


@router.get("/{tag_id}")
async def get_tag(
    tag_id: int,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    row = await repository.get_tag(tag_id, current_user.id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    links = await repository.list_tag_links(row.id)
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
            for link in links
        ],
    }
