from __future__ import annotations

from app.services.quality_hub.application.deployment_status import summarize_portfolio_status
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


async def get_portfolio_status(repository: QualityHubRepository, show_clusters: bool = False) -> list[dict]:
    deployments = await repository.list_deployments()
    payload = [
        {
            "project_id": row.project_id,
            "cluster_id": row.cluster_id,
            "env": row.env,
            "status": row.status,
            "project": str(row.project_id),
            "cluster": str(row.cluster_id),
            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        }
        for row in deployments
    ]
    return summarize_portfolio_status(payload, show_clusters=show_clusters)
