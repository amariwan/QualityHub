from __future__ import annotations

from app.services.quality_hub.infrastructure.tasks.sync_projects_task import sync_projects


def queue_project_sync(sync_run_id: int, user_id: int) -> str:
    job = sync_projects.delay(sync_run_id, user_id)
    return job.id
