from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db_session
from app.core.security.session_auth import get_current_user
from app.services.quality_hub.infrastructure.models import UserModel
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
async def auth_me(
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    repository = QualityHubRepository(session)
    credential = await repository.get_gitlab_credential(current_user.id)
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "gitlab_connected": credential is not None,
    }
