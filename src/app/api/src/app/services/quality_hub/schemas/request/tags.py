from pydantic import BaseModel


class TagLinkItem(BaseModel):
    scope_type: str = "PROJECT"
    project_id: int | None = None
    env: str | None = None
    cluster_id: int | None = None


class TagCreateRequest(BaseModel):
    visibility: str = "PRIVATE"
    team_id: int | None = None
    name: str
    color: str | None = None
    links: list[TagLinkItem] = []


class TagUpdateRequest(BaseModel):
    visibility: str | None = None
    team_id: int | None = None
    name: str | None = None
    color: str | None = None
    links: list[TagLinkItem] | None = None
