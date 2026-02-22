"""Reserved GraphQL adapter for future enrichment queries."""

from __future__ import annotations


class GitLabGraphQLClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def execute(self, token: str, query: str, variables: dict | None = None) -> dict:
        raise NotImplementedError("GraphQL integration is out of MVP scope")
