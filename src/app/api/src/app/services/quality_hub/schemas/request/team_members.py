from pydantic import BaseModel


class TeamMemberCreateRequest(BaseModel):
    user_id: int
    role: str = "member"


class TeamMemberUpdateRequest(BaseModel):
    role: str
