from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.application.teams import normalize_team_role
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.team_members import TeamMemberUpdateRequest

router = APIRouter(prefix="/teams/{team_id}/members", tags=["team-members"])


@router.put("/{member_id}")
async def update_team_member(
    team_id: int,
    member_id: int,
    payload: TeamMemberUpdateRequest,
    _: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    row = await repository.update_team_member(team_id, member_id, {"role": normalize_team_role(payload.role)})
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
    return {"id": row.id, "team_id": row.team_id, "user_id": row.user_id, "role": row.role}
