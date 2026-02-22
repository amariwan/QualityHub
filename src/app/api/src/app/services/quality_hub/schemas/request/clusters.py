from pydantic import BaseModel


class ClusterCreateRequest(BaseModel):
    name: str
    kube_api: str
    kube_context_ref: str
    kubeconfig_ref: str | None = None
    active: bool = True


class ClusterUpdateRequest(BaseModel):
    name: str | None = None
    kube_api: str | None = None
    kube_context_ref: str | None = None
    kubeconfig_ref: str | None = None
    active: bool | None = None
