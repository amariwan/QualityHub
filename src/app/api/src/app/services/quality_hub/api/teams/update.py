from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.teams import TeamUpdateRequest

router = APIRouter(prefix="/teams", tags=["teams"])


@router.put("/{team_id}")
async def update_team(
    team_id: int,
    payload: TeamUpdateRequest,
    _: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    row = await repository.update_team(team_id, payload.model_dump(exclude_none=True))
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return {"id": row.id, "name": row.name}
