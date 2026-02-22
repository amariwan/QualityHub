from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.projects_sync import ProjectsSyncRequest
from app.services.quality_hub.services.commands.sync_projects import queue_project_sync

router = APIRouter(prefix="/projects/sync", tags=["projects-sync"])


@router.post("")
async def create_project_sync(
    payload: ProjectsSyncRequest,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    sync_run = await repository.create_sync_run(current_user.id)
    celery_job_id = queue_project_sync(sync_run.id, current_user.id)
    return {
        "sync_run_id": sync_run.id,
        "celery_job_id": celery_job_id,
        "status": sync_run.status,
        "trigger": payload.trigger,
    }
