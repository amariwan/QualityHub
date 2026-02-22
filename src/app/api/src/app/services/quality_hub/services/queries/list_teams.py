from __future__ import annotations

from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


async def list_teams(repository: QualityHubRepository):
    return await repository.list_teams()
