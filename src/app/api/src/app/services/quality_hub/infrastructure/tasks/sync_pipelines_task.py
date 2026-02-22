from __future__ import annotations

import asyncio
from datetime import datetime

from celery import shared_task
from sqlalchemy import select

from app.core.db.session import AsyncSessionLocal
from app.core.security.token_cipher import TokenCipher
from app.services.quality_hub.application.gitlab_integration import list_project_pipelines
from app.services.quality_hub.infrastructure.models import GitlabCredentialModel, ProjectModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


async def _sync_pipelines_for_user(user_id: int) -> dict:
    async with AsyncSessionLocal() as session:
        repository = QualityHubRepository(session)
        credential = await repository.get_gitlab_credential(user_id)
        if credential is None:
            return {"synced_pipelines": 0, "reason": "missing_credentials"}

        cipher = TokenCipher()
        token = cipher.decrypt(credential.token_encrypted)
        projects = await repository.list_projects()

        synced = 0
        for project in projects:
            pipelines = await list_project_pipelines(
                token=token,
                base_url=credential.base_url,
                project_id=project.gitlab_project_id,
            )
            for pipeline in pipelines:
                await repository.upsert_pipeline(
                    project_id=project.id,
                    gitlab_pipeline_id=pipeline["id"],
                    ref=pipeline.get("ref"),
                    sha=pipeline.get("sha"),
                    status=pipeline.get("status", "unknown"),
                    started_at=_parse_datetime(pipeline.get("started_at")),
                    finished_at=_parse_datetime(pipeline.get("finished_at")),
                    duration=pipeline.get("duration"),
                    source_type=pipeline.get("source"),
                )
                synced += 1

        return {"synced_pipelines": synced}


@shared_task(name="quality_hub.sync_pipelines_user")
def sync_pipelines_user(user_id: int) -> dict:
    return asyncio.run(_sync_pipelines_for_user(user_id=user_id))


async def _sync_pipelines_all_users() -> dict:
    async with AsyncSessionLocal() as session:
        user_ids = (await session.execute(select(GitlabCredentialModel.user_id))).scalars().all()

    for user_id in user_ids:
        sync_pipelines_user.delay(user_id)

    return {"queued_users": len(user_ids)}


@shared_task(name="quality_hub.sync_pipelines_all")
def sync_pipelines_all() -> dict:
    return asyncio.run(_sync_pipelines_all_users())
