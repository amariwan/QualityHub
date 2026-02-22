from __future__ import annotations

from datetime import datetime

from app.services.quality_hub.infrastructure.adapters.gitlab_rest_client import GitLabRestClient


async def verify_token(*, token: str, base_url: str) -> dict:
    client = GitLabRestClient(base_url=base_url)
    return await client.get_user(token)


async def list_groups(*, token: str, base_url: str) -> list[dict]:
    client = GitLabRestClient(base_url=base_url)
    return await client.list_groups(token)


async def list_group_projects(*, token: str, base_url: str, group_id: int) -> list[dict]:
    client = GitLabRestClient(base_url=base_url)
    return await client.list_group_projects(token, group_id)


async def list_project_pipelines(*, token: str, base_url: str, project_id: int) -> list[dict]:
    client = GitLabRestClient(base_url=base_url)
    return await client.list_project_pipelines(token, project_id)


async def resolve_revision_metadata(*, token: str, base_url: str, project_id: int, sha: str | None) -> dict:
    if not sha:
        return {"actor_merger": None, "actor_author": None, "git_tag": None}

    client = GitLabRestClient(base_url=base_url)
    commit = await client.get_commit(token=token, project_id=project_id, sha=sha)
    merge_request = await client.get_merge_request_for_commit(token=token, project_id=project_id, sha=sha)
    tags = await client.list_tags_for_sha(token=token, project_id=project_id, sha=sha)

    actor_merger = None
    if merge_request:
        merged_by = merge_request.get("merged_by") or {}
        actor_merger = merged_by.get("username") or merged_by.get("name")

    actor_author = commit.get("author_email") or commit.get("author_name") if commit else None
    git_tag = tags[0].get("name") if tags else None

    return {
        "actor_merger": actor_merger,
        "actor_author": actor_author,
        "git_tag": git_tag,
        "resolved_at": datetime.utcnow().isoformat(),
    }
