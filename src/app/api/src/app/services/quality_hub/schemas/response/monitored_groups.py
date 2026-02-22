from pydantic import BaseModel


class MonitoredGroupResponse(BaseModel):
    id: int
    gitlab_group_id: int
    gitlab_group_path: str
