from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.services.queries.list_broken_pipelines import list_broken_pipelines

router = APIRouter(prefix="/pipelines", tags=["pipelines"])


@router.get("")
async def list_pipelines(
    scope: str = Query(default="all", pattern="^(all|readiness)$"),
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    rows = await list_broken_pipelines(repository, scope=scope)
    return {
        "scope": scope,
        "count": len(rows),
        "items": rows,
        "user_id": current_user.id,
    }
