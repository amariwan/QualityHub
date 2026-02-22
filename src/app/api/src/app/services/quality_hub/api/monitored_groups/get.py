from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/user/monitored-groups", tags=["monitored-groups"])


@router.get("/{monitored_group_id}")
async def get_monitored_group(
    monitored_group_id: int,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    item = await repository.get_monitored_group(monitored_group_id, current_user.id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Monitored group not found")
    return {"id": item.id, "gitlab_group_id": item.gitlab_group_id, "gitlab_group_path": item.gitlab_group_path}
