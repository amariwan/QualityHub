from __future__ import annotations

from celery import Celery

from app.config.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "quality_hub",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    timezone="UTC",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
)

celery_app.autodiscover_tasks(
    [
        "app.services.quality_hub.infrastructure.tasks.sync_projects_task",
        "app.services.quality_hub.infrastructure.tasks.sync_pipelines_task",
        "app.services.quality_hub.infrastructure.tasks.watch_cluster_task",
        "app.services.quality_hub.infrastructure.tasks.reconcile_deployments_task",
    ]
)
