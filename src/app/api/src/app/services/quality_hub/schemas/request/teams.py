from pydantic import BaseModel


class TeamCreateRequest(BaseModel):
    name: str


class TeamUpdateRequest(BaseModel):
    name: str | None = None
