from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Pipeline:
    id: int
    project_id: int
    gitlab_pipeline_id: int
    status: str
    ref: str | None
    sha: str | None
    source_type: str | None
