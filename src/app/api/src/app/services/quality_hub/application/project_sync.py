from __future__ import annotations

from app.services.quality_hub.application.gitlab_integration import list_group_projects
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


async def sync_projects_for_groups(
    *,
    repository: QualityHubRepository,
    token: str,
    base_url: str,
    monitored_groups: list[dict],
) -> int:
    synced = 0
    for group in monitored_groups:
        group_id = int(group["gitlab_group_id"])
        projects = await list_group_projects(token=token, base_url=base_url, group_id=group_id)
        for project in projects:
            await repository.upsert_project(
                gitlab_project_id=project["id"],
                path_with_namespace=project.get("path_with_namespace", str(project["id"])),
                default_branch=project.get("default_branch"),
            )
            synced += 1
    return synced
