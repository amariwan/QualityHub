from __future__ import annotations

from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


async def create_note(repository: QualityHubRepository, payload: dict):
    return await repository.create_note(**payload)
