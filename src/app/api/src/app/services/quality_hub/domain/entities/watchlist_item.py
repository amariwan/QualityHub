from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WatchlistItem:
    id: int
    owner_user_id: int
    project_id: int
    visibility: str
