from __future__ import annotations


def ensure_visibility(visibility: str) -> str:
    if visibility not in {"PRIVATE", "TEAM"}:
        raise ValueError("visibility must be PRIVATE or TEAM")
    return visibility
