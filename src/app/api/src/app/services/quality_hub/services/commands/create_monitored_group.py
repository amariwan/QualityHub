from __future__ import annotations

from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


async def create_monitored_group(repository: QualityHubRepository, user_id: int, gitlab_group_id: int, gitlab_group_path: str):
    return await repository.create_monitored_group(
        user_id=user_id,
        gitlab_group_id=gitlab_group_id,
        gitlab_group_path=gitlab_group_path,
    )
