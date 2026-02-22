from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.api.monitored_groups.update import update_monitored_group
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.schemas.request.monitored_groups import MonitoredGroupPatchRequest

router = APIRouter(prefix="/user/monitored-groups", tags=["monitored-groups"])


@router.patch("/{monitored_group_id}")
async def patch_monitored_group(
    monitored_group_id: int,
    payload: MonitoredGroupPatchRequest,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
):
    return await update_monitored_group(
        monitored_group_id=monitored_group_id,
        payload=payload,
        current_user=current_user,
        session=session,
    )
