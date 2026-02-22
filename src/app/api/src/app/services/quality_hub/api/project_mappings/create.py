from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.project_mappings import ProjectMappingCreateRequest

router = APIRouter(prefix="/project-mappings", tags=["project-mappings"])


@router.post("")
async def create_project_mapping(
    payload: ProjectMappingCreateRequest,
    _: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    item = await repository.create_project_mapping(**payload.model_dump())
    return {
        "id": item.id,
        "project_id": item.project_id,
        "cluster_id": item.cluster_id,
        "namespace": item.namespace,
        "kind": item.kind,
        "resource_name": item.resource_name,
        "env_override": item.env_override,
        "enabled": item.enabled,
    }
