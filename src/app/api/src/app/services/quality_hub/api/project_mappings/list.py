from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/project-mappings", tags=["project-mappings"])


@router.get("")
async def list_project_mappings(
    _: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> list[dict]:
    repository = QualityHubRepository(session)
    rows = await repository.list_project_mappings()
    return [
        {
            "id": row.id,
            "project_id": row.project_id,
            "cluster_id": row.cluster_id,
            "namespace": row.namespace,
            "kind": row.kind,
            "resource_name": row.resource_name,
            "env_override": row.env_override,
            "enabled": row.enabled,
        }
        for row in rows
    ]
