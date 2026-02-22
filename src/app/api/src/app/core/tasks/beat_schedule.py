from __future__ import annotations

from celery.schedules import crontab

from app.core.tasks.celery_app import celery_app

celery_app.conf.beat_schedule = {
    "projects-sync-every-5-min": {
        "task": "quality_hub.sync_projects_all",
        "schedule": crontab(minute="*/5"),
    },
    "pipelines-sync-every-2-min": {
        "task": "quality_hub.sync_pipelines_all",
        "schedule": crontab(minute="*/2"),
    },
    "watch-supervision-every-min": {
        "task": "quality_hub.reconcile_deployments",
        "schedule": crontab(minute="*"),
    },
}
