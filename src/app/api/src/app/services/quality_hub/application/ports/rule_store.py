"""Port interface defining persistence operations for rules."""

from __future__ import annotations

from typing import Protocol

class RuleStore(Protocol):
    async def save(self, rule: "Rule") -> None:  # type: ignore[name-defined]
        ...

    async def get(self, rule_id: str) -> "Rule":  # type: ignore[name-defined]
        ...

    async def list(self) -> list["Rule"]:  # type: ignore[name-defined]
        ...

    async def delete(self, rule_id: str) -> None:
        ...
