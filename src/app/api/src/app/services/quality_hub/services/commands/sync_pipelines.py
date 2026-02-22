from __future__ import annotations

from app.services.quality_hub.infrastructure.tasks.sync_pipelines_task import sync_pipelines_user


def queue_pipeline_sync(user_id: int) -> str:
    job = sync_pipelines_user.delay(user_id)
    return job.id
