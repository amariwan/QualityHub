from __future__ import annotations

from app.services.quality_hub.application.deployment_status import build_project_matrix
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


async def get_project_status(repository: QualityHubRepository, project_id: int) -> dict:
    deployments = await repository.list_deployments(project_id=project_id)
    payload = [
        {
            "deployment_id": row.id,
            "project_id": row.project_id,
            "cluster_id": row.cluster_id,
            "env": row.env,
            "status": row.status,
            "kind": row.kind,
            "namespace": row.namespace,
            "resource_name": row.resource_name,
            "last_deploy_at": row.last_deploy_at.isoformat() if row.last_deploy_at else None,
            "git_revision": row.git_revision,
            "git_tag": row.git_tag,
            "image_ref": row.image_ref,
            "image_digest": row.image_digest,
            "helm_chart": row.helm_chart,
            "helm_chart_version": row.helm_chart_version,
            "actor_merger": row.actor_merger,
            "actor_author": row.actor_author,
            "message": row.message,
            "updated_at": row.updated_at.isoformat() if row.updated_at else None,
        }
        for row in deployments
    ]
    return {"project_id": project_id, "matrix": build_project_matrix(payload)}
