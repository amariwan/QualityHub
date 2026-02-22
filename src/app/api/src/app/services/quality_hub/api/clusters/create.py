from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.infrastructure.tasks.watch_cluster_task import watch_cluster
from app.services.quality_hub.schemas.request.clusters import ClusterCreateRequest

router = APIRouter(prefix="/clusters", tags=["clusters"])


@router.post("")
async def create_cluster(
    payload: ClusterCreateRequest,
    _: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    item = await repository.create_cluster(**payload.model_dump())
    if item.active:
        watch_cluster.delay(item.id)
    return {
        "id": item.id,
        "name": item.name,
        "kube_api": item.kube_api,
        "kube_context_ref": item.kube_context_ref,
        "kubeconfig_ref": item.kubeconfig_ref,
        "active": item.active,
    }
