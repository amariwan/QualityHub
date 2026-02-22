from __future__ import annotations

import asyncio
from datetime import datetime, timedelta

from celery import shared_task
from sqlalchemy import select, update

from app.config.settings import get_settings
from app.core.db.session import AsyncSessionLocal
from app.services.quality_hub.infrastructure.models import DeploymentModel, WatchLeaseModel


async def _reconcile_stale_status() -> dict:
    settings = get_settings()
    cutoff = datetime.utcnow() - timedelta(seconds=settings.WATCH_STALE_TTL_SECONDS)

    async with AsyncSessionLocal() as session:
        stale_cluster_ids = (
            await session.execute(
                select(WatchLeaseModel.cluster_id).where(
                    (WatchLeaseModel.heartbeat_at < cutoff) | (WatchLeaseModel.stale.is_(True))
                )
            )
        ).scalars().all()

        if stale_cluster_ids:
            await session.execute(
                update(DeploymentModel)
                .where(DeploymentModel.cluster_id.in_(stale_cluster_ids))
                .values(status="unknown", updated_at=datetime.utcnow())
            )
            await session.commit()

    return {"stale_clusters": len(stale_cluster_ids)}


@shared_task(name="quality_hub.reconcile_deployments")
def reconcile_deployments() -> dict:
    return asyncio.run(_reconcile_stale_status())
