from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.application.teams import normalize_team_role
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.team_members import TeamMemberCreateRequest

router = APIRouter(prefix="/teams/{team_id}/members", tags=["team-members"])


@router.post("")
async def create_team_member(
    team_id: int,
    payload: TeamMemberCreateRequest,
    _: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)

    team = await repository.get_team(team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    user = await repository.get_user(payload.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    row = await repository.add_team_member(team_id=team_id, user_id=payload.user_id, role=normalize_team_role(payload.role))
    return {"id": row.id, "team_id": row.team_id, "user_id": row.user_id, "role": row.role}
