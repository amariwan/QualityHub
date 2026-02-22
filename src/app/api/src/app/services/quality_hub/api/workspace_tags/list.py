from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/workspace/tags", tags=["workspace-tags"])


@router.get("")
async def list_tags(
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> list[dict]:
    repository = QualityHubRepository(session)
    rows = await repository.list_tags(current_user.id)
    output = []
    for row in rows:
        links = await repository.list_tag_links(row.id)
        output.append(
            {
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
        )
    return output
