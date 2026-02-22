from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.domain.validators import ensure_visibility
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.tags import TagCreateRequest

router = APIRouter(prefix="/workspace/tags", tags=["workspace-tags"])


@router.post("")
async def create_tag(
    payload: TagCreateRequest,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    tag = await repository.create_tag(
        owner_user_id=current_user.id,
        visibility=ensure_visibility(payload.visibility),
        team_id=payload.team_id,
        name=payload.name,
        color=payload.color,
    )
    await repository.replace_tag_links(tag.id, [link.model_dump() for link in payload.links])
    links = await repository.list_tag_links(tag.id)
    return {
        "id": tag.id,
        "visibility": tag.visibility,
        "team_id": tag.team_id,
        "name": tag.name,
        "color": tag.color,
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
