from __future__ import annotations

from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


async def list_workspace_views(repository: QualityHubRepository, owner_user_id: int):
    return await repository.list_workspace_views(owner_user_id)
