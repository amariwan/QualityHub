from __future__ import annotations

import asyncio

from celery import shared_task
from sqlalchemy import select

from app.core.db.session import AsyncSessionLocal
from app.services.quality_hub.application.project_sync import sync_projects_for_groups
from app.services.quality_hub.infrastructure.models import GitlabCredentialModel, MonitoredGroupModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.core.security.token_cipher import TokenCipher


async def _sync_projects_for_user(sync_run_id: int, user_id: int) -> dict:
    async with AsyncSessionLocal() as session:
        repository = QualityHubRepository(session)
        cipher = TokenCipher()

        credential = await repository.get_gitlab_credential(user_id)
        if credential is None:
            await repository.update_sync_run(sync_run_id, "failed", "No GitLab credential configured")
            return {"synced_projects": 0}

        groups = await repository.list_monitored_groups(user_id)
        payload_groups = [
            {
                "gitlab_group_id": item.gitlab_group_id,
                "gitlab_group_path": item.gitlab_group_path,
            }
            for item in groups
        ]

        if not payload_groups:
            await repository.update_sync_run(sync_run_id, "done", "No monitored groups")
            return {"synced_projects": 0}

        token = cipher.decrypt(credential.token_encrypted)
        await repository.update_sync_run(sync_run_id, "running", "Sync started")
        synced = await sync_projects_for_groups(
            repository=repository,
            token=token,
            base_url=credential.base_url,
            monitored_groups=payload_groups,
        )
        await repository.update_sync_run(sync_run_id, "done", f"Synced {synced} projects")
        return {"synced_projects": synced}


@shared_task(name="quality_hub.sync_projects")
def sync_projects(sync_run_id: int, user_id: int) -> dict:
    return asyncio.run(_sync_projects_for_user(sync_run_id=sync_run_id, user_id=user_id))


async def _sync_all_users() -> dict:
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(select(GitlabCredentialModel.user_id))).scalars().all()

    for user_id in rows:
        async with AsyncSessionLocal() as session:
            repository = QualityHubRepository(session)
            run = await repository.create_sync_run(user_id)
        sync_projects.delay(run.id, user_id)

    return {"queued_users": len(rows)}


@shared_task(name="quality_hub.sync_projects_all")
def sync_projects_all() -> dict:
    return asyncio.run(_sync_all_users())
