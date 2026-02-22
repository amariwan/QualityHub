from __future__ import annotations


def can_read_item(*, owner_user_id: int, current_user_id: int, visibility: str, team_id: int | None, user_team_ids: set[int]) -> bool:
    if owner_user_id == current_user_id:
        return True
    if visibility == "TEAM" and team_id is not None and team_id in user_team_ids:
        return True
    return False
