from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.infrastructure.tasks.watch_cluster_task import watch_cluster
from app.services.quality_hub.schemas.request.clusters import ClusterUpdateRequest

router = APIRouter(prefix="/clusters", tags=["clusters"])


@router.put("/{cluster_id}")
async def update_cluster(
    cluster_id: int,
    payload: ClusterUpdateRequest,
    _: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    row = await repository.update_cluster(cluster_id, payload.model_dump(exclude_none=True))
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cluster not found")
    if row.active:
        watch_cluster.delay(row.id)
    return {
        "id": row.id,
        "name": row.name,
        "kube_api": row.kube_api,
        "kube_context_ref": row.kube_context_ref,
        "kubeconfig_ref": row.kubeconfig_ref,
        "active": row.active,
    }
