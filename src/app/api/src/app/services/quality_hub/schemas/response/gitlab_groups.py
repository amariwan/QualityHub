from pydantic import BaseModel


class GitLabGroupResponse(BaseModel):
    id: int
    path: str
    full_path: str
    name: str
