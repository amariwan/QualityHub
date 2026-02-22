from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/clusters", tags=["clusters"])


@router.get("/{cluster_id}")
async def get_cluster(
    cluster_id: int,
    _: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    row = await repository.get_cluster(cluster_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cluster not found")
    return {
        "id": row.id,
        "name": row.name,
        "kube_api": row.kube_api,
        "kube_context_ref": row.kube_context_ref,
        "kubeconfig_ref": row.kubeconfig_ref,
        "active": row.active,
    }
