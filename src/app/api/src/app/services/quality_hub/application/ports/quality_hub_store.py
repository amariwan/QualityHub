from __future__ import annotations

from typing import Protocol


class QualityHubStorePort(Protocol):
    async def upsert_deployment(self, key: dict, payload: dict): ...
