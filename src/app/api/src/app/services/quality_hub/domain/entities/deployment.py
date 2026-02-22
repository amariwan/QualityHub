from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Deployment:
    id: int
    project_id: int
    cluster_id: int
    env: str
    status: str
    resource_name: str
