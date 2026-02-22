from pydantic import BaseModel


class WatchlistResponse(BaseModel):
    id: int
    visibility: str
    project_id: int
