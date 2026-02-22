from pydantic import BaseModel


class PipelinesFilterRequest(BaseModel):
    scope: str = "all"
    status: str | None = None
    project_id: int | None = None
    ref: str | None = None
    source_type: str | None = None
