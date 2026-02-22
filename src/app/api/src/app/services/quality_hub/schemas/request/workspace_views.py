from pydantic import BaseModel


class WorkspaceViewCreateRequest(BaseModel):
    name: str
    visibility: str = "PRIVATE"
    team_id: int | None = None
    definition_json: dict = {}


class WorkspaceViewUpdateRequest(BaseModel):
    name: str | None = None
    visibility: str | None = None
    team_id: int | None = None
    definition_json: dict | None = None
