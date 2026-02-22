from pydantic import BaseModel


class WatchlistCreateRequest(BaseModel):
    visibility: str = "PRIVATE"
    team_id: int | None = None
    project_id: int


class WatchlistUpdateRequest(BaseModel):
    visibility: str | None = None
    team_id: int | None = None
    project_id: int | None = None
