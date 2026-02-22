from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/projects/sync", tags=["projects-sync"])


@router.get("/{sync_run_id}")
async def get_project_sync(
    sync_run_id: int,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    sync_run = await repository.get_sync_run(sync_run_id, current_user.id)
    if sync_run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sync run not found")
    return {
        "id": sync_run.id,
        "status": sync_run.status,
        "message": sync_run.message,
        "created_at": sync_run.created_at.isoformat() if sync_run.created_at else None,
        "updated_at": sync_run.updated_at.isoformat() if sync_run.updated_at else None,
    }
