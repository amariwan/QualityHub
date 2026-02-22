from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/user/monitored-groups", tags=["monitored-groups"])


@router.get("")
async def list_monitored_groups(
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> list[dict]:
    repository = QualityHubRepository(session)
    rows = await repository.list_monitored_groups(current_user.id)
    return [
        {"id": row.id, "gitlab_group_id": row.gitlab_group_id, "gitlab_group_path": row.gitlab_group_path}
        for row in rows
    ]
