from pydantic import BaseModel


class DeploymentClusterStatus(BaseModel):
    cluster_id: int
    cluster: str | None
    status: str
    updated_at: str | None


class DeploymentEnvironmentStatus(BaseModel):
    env: str
    status: str
    clusters: list[DeploymentClusterStatus]


class PortfolioDeploymentResponse(BaseModel):
    project_id: int
    project: str | None
    environments: list[DeploymentEnvironmentStatus]
