from __future__ import annotations

from app.services.quality_hub.application.teams import normalize_team_role
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


async def add_team_member(repository: QualityHubRepository, team_id: int, user_id: int, role: str):
    return await repository.add_team_member(team_id=team_id, user_id=user_id, role=normalize_team_role(role))
