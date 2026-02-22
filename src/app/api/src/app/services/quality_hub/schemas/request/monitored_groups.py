from pydantic import BaseModel, Field


class MonitoredGroupUpsertRequest(BaseModel):
    gitlab_group_id: int | None = None
    gitlab_group_path: str | None = None
    group_url: str | None = None


class MonitoredGroupPatchRequest(BaseModel):
    gitlab_group_id: int | None = None
    gitlab_group_path: str | None = None
    group_url: str | None = None
