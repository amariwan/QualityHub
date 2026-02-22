from pydantic import BaseModel


class WorkspaceViewResponse(BaseModel):
    id: int
    name: str
    visibility: str
    team_id: int | None
    definition_json: dict
