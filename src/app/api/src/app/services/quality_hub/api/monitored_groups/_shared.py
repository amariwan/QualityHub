from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.token_cipher import TokenCipher
from app.services.quality_hub.api._utils import parse_group_reference
from app.services.quality_hub.application.gitlab_integration import list_groups
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


async def resolve_group_identity(
    *,
    session: AsyncSession,
    user_id: int,
    gitlab_group_id: int | None,
    gitlab_group_path: str | None,
    group_url: str | None,
) -> tuple[int, str]:
    if group_url and not gitlab_group_path:
        gitlab_group_path = parse_group_reference(group_url)

    if gitlab_group_id and gitlab_group_path:
        return gitlab_group_id, gitlab_group_path

    repository = QualityHubRepository(session)
    credential = await repository.get_gitlab_credential(user_id)
    if credential is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="GitLab token is not connected")

    token = TokenCipher().decrypt(credential.token_encrypted)
    groups = await list_groups(token=token, base_url=credential.base_url)

    if gitlab_group_id:
        for group in groups:
            if group.get("id") == gitlab_group_id:
                return gitlab_group_id, group.get("full_path") or group.get("path") or str(gitlab_group_id)

    if gitlab_group_path:
        for group in groups:
            full_path = group.get("full_path") or group.get("path")
            if full_path == gitlab_group_path:
                return group["id"], full_path

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to resolve group")
