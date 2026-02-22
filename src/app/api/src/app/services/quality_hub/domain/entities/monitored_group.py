from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MonitoredGroup:
    id: int
    user_id: int
    gitlab_group_id: int
    gitlab_group_path: str
