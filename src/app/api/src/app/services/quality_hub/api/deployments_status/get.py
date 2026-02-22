from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.services.queries.get_project_status import get_project_status

router = APIRouter(prefix="/deployments/status", tags=["deployments"])


@router.get("/{project_id}")
async def get_deployment_status(
    project_id: int,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    payload = await get_project_status(repository, project_id)
    payload["user_id"] = current_user.id
    return payload
