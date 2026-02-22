from pydantic import BaseModel


class AuthMeResponse(BaseModel):
    user_id: int
    email: str
    name: str | None
    gitlab_connected: bool
