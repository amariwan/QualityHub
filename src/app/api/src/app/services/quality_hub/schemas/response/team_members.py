from pydantic import BaseModel


class TeamMemberResponse(BaseModel):
    id: int
    team_id: int
    user_id: int
    role: str
