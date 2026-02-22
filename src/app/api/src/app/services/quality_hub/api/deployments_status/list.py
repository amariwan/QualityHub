from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.services.queries.get_portfolio_status import get_portfolio_status

router = APIRouter(prefix="/deployments/status", tags=["deployments"])


@router.get("")
async def list_deployment_status(
    show_clusters: bool = Query(default=False),
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    items = await get_portfolio_status(repository, show_clusters=show_clusters)
    return {
        "user_id": current_user.id,
        "show_clusters": show_clusters,
        "items": items,
    }
