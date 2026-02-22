from pydantic import BaseModel


class ProjectMappingCreateRequest(BaseModel):
    project_id: int
    cluster_id: int
    namespace: str
    kind: str
    resource_name: str
    env_override: str | None = None
    enabled: bool = True


class ProjectMappingUpdateRequest(BaseModel):
    namespace: str | None = None
    kind: str | None = None
    resource_name: str | None = None
    env_override: str | None = None
    enabled: bool | None = None
