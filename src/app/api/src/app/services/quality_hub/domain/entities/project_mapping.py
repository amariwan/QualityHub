from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ProjectMapping:
    id: int
    project_id: int
    cluster_id: int
    namespace: str
    kind: str
    resource_name: str
    env_override: str | None
