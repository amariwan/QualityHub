from __future__ import annotations


async def upsert_deployment(store, normalized: dict):
    key = {
        "project_id": normalized["project_id"],
        "cluster_id": normalized["cluster_id"],
        "env": normalized["env"],
        "kind": normalized["kind"],
        "namespace": normalized["namespace"],
        "resource_name": normalized["resource_name"],
    }
    payload = {
        "status": normalized.get("status", "unknown"),
        "last_deploy_at": normalized.get("last_deploy_at"),
        "git_revision": normalized.get("git_revision"),
        "git_tag": normalized.get("git_tag"),
        "image_ref": normalized.get("image_ref"),
        "image_digest": normalized.get("image_digest"),
        "helm_chart": normalized.get("helm_chart"),
        "helm_chart_version": normalized.get("helm_chart_version"),
        "actor_merger": normalized.get("actor_merger"),
        "actor_author": normalized.get("actor_author"),
        "message": normalized.get("message"),
    }
    return await store.upsert_deployment(key=key, payload=payload)
