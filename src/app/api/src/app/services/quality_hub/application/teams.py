from __future__ import annotations


def normalize_team_role(role: str) -> str:
    normalized = role.strip().lower()
    if normalized not in {"owner", "admin", "member"}:
        raise ValueError("role must be one of owner, admin, member")
    return normalized
