from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WorkspaceView:
    id: int
    owner_user_id: int
    name: str
    visibility: str
    definition_json: dict
