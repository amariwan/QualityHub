from __future__ import annotations

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.core.db.session import get_db_session
from app.core.security.session_auth import create_session
from app.core.security.token_cipher import TokenCipher
from app.services.quality_hub.application.gitlab_integration import verify_token
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository
from app.services.quality_hub.schemas.request.auth_token import ConnectTokenRequest

router = APIRouter(prefix="/auth/token", tags=["auth"])


@router.post("")
async def connect_token(
    payload: ConnectTokenRequest,
    response: Response,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    settings = get_settings()
    base_url = payload.base_url or settings.GITLAB_BASE_URL
    gitlab_user = await verify_token(token=payload.token, base_url=base_url)

    email = gitlab_user.get("email") or f"{gitlab_user.get('username')}@gitlab.local"
    name = gitlab_user.get("name")
    auth_provider_id = str(gitlab_user.get("id"))

    repository = QualityHubRepository(session)
    user = await repository.upsert_user(email=email, name=name, auth_provider_id=auth_provider_id)

    cipher = TokenCipher()
    await repository.upsert_gitlab_credential(
        user_id=user.id,
        gitlab_user_id=gitlab_user["id"],
        base_url=base_url,
        token_encrypted=cipher.encrypt(payload.token),
    )

    create_session(response, user.id)

    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "gitlab_connected": True,
    }
