from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.project_mappings import ProjectMappingUpdateRequest

router = APIRouter(prefix="/project-mappings", tags=["project-mappings"])


@router.put("/{mapping_id}")
async def update_project_mapping(
    mapping_id: int,
    payload: ProjectMappingUpdateRequest,
    _: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    row = await repository.update_project_mapping(mapping_id, payload.model_dump(exclude_none=True))
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project mapping not found")
    return {
        "id": row.id,
        "project_id": row.project_id,
        "cluster_id": row.cluster_id,
        "namespace": row.namespace,
        "kind": row.kind,
        "resource_name": row.resource_name,
        "env_override": row.env_override,
        "enabled": row.enabled,
    }
