from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.api.monitored_groups._shared import resolve_group_identity
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.monitored_groups import MonitoredGroupUpsertRequest

router = APIRouter(prefix="/user/monitored-groups", tags=["monitored-groups"])


@router.put("/{monitored_group_id}")
async def update_monitored_group(
    monitored_group_id: int,
    payload: MonitoredGroupUpsertRequest,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    group_id, group_path = await resolve_group_identity(
        session=session,
        user_id=current_user.id,
        gitlab_group_id=payload.gitlab_group_id,
        gitlab_group_path=payload.gitlab_group_path,
        group_url=payload.group_url,
    )

    repository = QualityHubRepository(session)
    item = await repository.update_monitored_group(
        monitored_group_id=monitored_group_id,
        user_id=current_user.id,
        gitlab_group_id=group_id,
        gitlab_group_path=group_path,
    )
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Monitored group not found")

    return {"id": item.id, "gitlab_group_id": item.gitlab_group_id, "gitlab_group_path": item.gitlab_group_path}
