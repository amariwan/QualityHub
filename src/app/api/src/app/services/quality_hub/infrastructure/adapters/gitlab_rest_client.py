from __future__ import annotations

from urllib.parse import quote

import httpx

from app.config.settings import get_settings


class GitLabRestClient:
    def __init__(self, base_url: str | None = None, timeout_seconds: float = 20.0):
        settings = get_settings()
        root = (base_url or settings.GITLAB_BASE_URL).rstrip("/")
        self.api_base_url = f"{root}/api/v4"
        self.timeout_seconds = timeout_seconds

    async def _request(self, method: str, path: str, token: str, params: dict | None = None) -> dict | list:
        headers = {"PRIVATE-TOKEN": token}
        url = f"{self.api_base_url}{path}"
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.request(method, url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

    async def get_user(self, token: str) -> dict:
        result = await self._request("GET", "/user", token)
        if not isinstance(result, dict):
            raise ValueError("Unexpected GitLab user response")
        return result

    async def list_groups(self, token: str) -> list[dict]:
        result = await self._request("GET", "/groups", token, params={"per_page": 100})
        return [item for item in result if isinstance(item, dict)]

    async def get_group(self, token: str, group_id: int) -> dict:
        result = await self._request("GET", f"/groups/{group_id}", token)
        if not isinstance(result, dict):
            raise ValueError("Unexpected GitLab group response")
        return result

    async def list_group_projects(self, token: str, group_id: int) -> list[dict]:
        result = await self._request(
            "GET",
            f"/groups/{group_id}/projects",
            token,
            params={"per_page": 100, "include_subgroups": "true"},
        )
        return [item for item in result if isinstance(item, dict)]

    async def list_project_pipelines(self, token: str, project_id: int) -> list[dict]:
        result = await self._request(
            "GET",
            f"/projects/{project_id}/pipelines",
            token,
            params={"per_page": 50},
        )
        return [item for item in result if isinstance(item, dict)]

    async def get_pipeline(self, token: str, project_id: int, pipeline_id: int) -> dict:
        result = await self._request("GET", f"/projects/{project_id}/pipelines/{pipeline_id}", token)
        if not isinstance(result, dict):
            raise ValueError("Unexpected pipeline response")
        return result

    async def get_pipeline_test_report_summary(self, token: str, project_id: int, pipeline_id: int) -> dict | None:
        try:
            result = await self._request(
                "GET",
                f"/projects/{project_id}/pipelines/{pipeline_id}/test_report_summary",
                token,
            )
            return result if isinstance(result, dict) else None
        except httpx.HTTPStatusError:
            return None

    async def get_commit(self, token: str, project_id: int, sha: str) -> dict | None:
        try:
            encoded = quote(sha, safe="")
            result = await self._request("GET", f"/projects/{project_id}/repository/commits/{encoded}", token)
            return result if isinstance(result, dict) else None
        except httpx.HTTPStatusError:
            return None

    async def get_merge_request_for_commit(self, token: str, project_id: int, sha: str) -> dict | None:
        try:
            encoded = quote(sha, safe="")
            result = await self._request(
                "GET",
                f"/projects/{project_id}/repository/commits/{encoded}/merge_requests",
                token,
                params={"per_page": 1},
            )
            if isinstance(result, list) and result:
                first = result[0]
                return first if isinstance(first, dict) else None
            return None
        except httpx.HTTPStatusError:
            return None

    async def list_tags_for_sha(self, token: str, project_id: int, sha: str) -> list[dict]:
        try:
            tags = await self._request("GET", f"/projects/{project_id}/repository/tags", token, params={"per_page": 100})
            output: list[dict] = []
            if isinstance(tags, list):
                for tag in tags:
                    if not isinstance(tag, dict):
                        continue
                    commit = tag.get("commit") or {}
                    if isinstance(commit, dict) and commit.get("id") == sha:
                        output.append(tag)
            return output
        except httpx.HTTPStatusError:
            return []
