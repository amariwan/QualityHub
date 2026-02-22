"""SQLAlchemy implementation of the RuleStore interface.

Use an AsyncSession from SQLAlchemy for persistence operations.
"""

from __future__ import annotations

from ...application.ports.rule_store import RuleStore

class SQLRuleRepository(RuleStore):
    def __init__(self, session):
        self.session = session  # type: ignore

    async def save(self, rule):
        ...

    async def get(self, rule_id: str):
        ...

    async def list(self):
        ...

    async def delete(self, rule_id: str):
        ...
