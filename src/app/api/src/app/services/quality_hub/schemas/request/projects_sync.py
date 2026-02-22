from pydantic import BaseModel


class ProjectsSyncRequest(BaseModel):
    trigger: str = "manual"
