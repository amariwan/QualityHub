from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.api.monitored_groups._shared import resolve_group_identity
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.monitored_groups import MonitoredGroupUpsertRequest

router = APIRouter(prefix="/user/monitored-groups", tags=["monitored-groups"])


@router.post("")
async def create_monitored_group(
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
    try:
        item = await repository.create_monitored_group(
            user_id=current_user.id,
            gitlab_group_id=group_id,
            gitlab_group_path=group_path,
        )
    except IntegrityError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Monitored group already exists") from exc

    return {"id": item.id, "gitlab_group_id": item.gitlab_group_id, "gitlab_group_path": item.gitlab_group_path}
