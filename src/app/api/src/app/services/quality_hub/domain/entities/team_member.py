from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TeamMember:
    id: int
    team_id: int
    user_id: int
    role: str
