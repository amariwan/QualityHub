from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Project:
    id: int
    gitlab_project_id: int
    path_with_namespace: str
    default_branch: str | None
