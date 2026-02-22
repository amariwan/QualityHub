from __future__ import annotations

import asyncio
import socket

from celery import shared_task

from app.core.db.session import AsyncSessionLocal
from app.services.quality_hub.infrastructure.adapters import KubernetesFluxWatchAdapter
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.services.commands.upsert_deployment import upsert_deployment


async def _watch_cluster(cluster_id: int) -> dict:
    worker_id = socket.gethostname()

    async with AsyncSessionLocal() as session:
        repository = QualityHubRepository(session)
        cluster = await repository.get_cluster(cluster_id)
        if cluster is None or not cluster.active:
            return {"status": "skipped", "reason": "cluster_missing_or_inactive"}

        await repository.upsert_watch_lease(cluster_id=cluster.id, worker_id=worker_id)

    adapter = KubernetesFluxWatchAdapter()

    try:
        for event in adapter.stream_flux_events({"id": cluster_id}):
            async with AsyncSessionLocal() as session:
                repository = QualityHubRepository(session)
                await repository.upsert_watch_lease(cluster_id=cluster_id, worker_id=worker_id)

                if event.get("kind") == "heartbeat":
                    continue

                await upsert_deployment(repository, event)
    except Exception:
        async with AsyncSessionLocal() as session:
            repository = QualityHubRepository(session)
            await repository.mark_watch_stale(cluster_id)
        raise

    return {"status": "completed"}


@shared_task(bind=True, name="quality_hub.watch_cluster", acks_late=False)
def watch_cluster(self, cluster_id: int) -> dict:
    return asyncio.run(_watch_cluster(cluster_id=cluster_id))
