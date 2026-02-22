from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Tag:
    id: int
    owner_user_id: int
    name: str
    visibility: str
    color: str | None
