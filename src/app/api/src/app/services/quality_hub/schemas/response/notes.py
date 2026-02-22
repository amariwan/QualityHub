from pydantic import BaseModel


class NoteResponse(BaseModel):
    id: int
    visibility: str
    scope_type: str
    content: str
    project_id: int | None
    env: str | None
    cluster_id: int | None
