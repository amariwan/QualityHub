from __future__ import annotations

from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


async def create_team(repository: QualityHubRepository, name: str):
    return await repository.create_team(name=name)
