from pydantic import BaseModel


class TagLinkResponse(BaseModel):
    id: int
    scope_type: str
    project_id: int | None
    env: str | None
    cluster_id: int | None


class TagResponse(BaseModel):
    id: int
    visibility: str
    team_id: int | None
    name: str
    color: str | None
    links: list[TagLinkResponse]
