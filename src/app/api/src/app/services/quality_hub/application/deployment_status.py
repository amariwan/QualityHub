from __future__ import annotations

from collections import defaultdict


def summarize_portfolio_status(deployments: list[dict], show_clusters: bool = False) -> list[dict]:
    grouped: dict[int, dict] = {}

    for item in deployments:
        project_id = item["project_id"]
        project = grouped.setdefault(
            project_id,
            {
                "project_id": project_id,
                "project": item.get("project"),
                "environments": defaultdict(lambda: {"statuses": [], "clusters": []}),
            },
        )
        env_block = project["environments"][item["env"]]
        env_block["statuses"].append(item["status"])
        if show_clusters:
            env_block["clusters"].append(
                {
                    "cluster_id": item["cluster_id"],
                    "cluster": item.get("cluster"),
                    "status": item["status"],
                    "updated_at": item.get("updated_at"),
                }
            )

    payload: list[dict] = []
    for project in grouped.values():
        env_payload = []
        for env, data in project["environments"].items():
            statuses = data["statuses"]
            env_status = "unknown"
            if statuses:
                if "failed" in statuses:
                    env_status = "failed"
                elif "degraded" in statuses:
                    env_status = "degraded"
                elif "progressing" in statuses:
                    env_status = "progressing"
                elif all(status == "ready" for status in statuses):
                    env_status = "ready"
            env_payload.append(
                {
                    "env": env,
                    "status": env_status,
                    "clusters": data["clusters"] if show_clusters else [],
                }
            )
        payload.append(
            {
                "project_id": project["project_id"],
                "project": project["project"],
                "environments": sorted(env_payload, key=lambda x: x["env"]),
            }
        )

    return sorted(payload, key=lambda x: x["project"] or "")


def build_project_matrix(deployments: list[dict]) -> dict:
    matrix: dict[str, list[dict]] = defaultdict(list)
    for item in deployments:
        matrix[item["env"]].append(item)
    return {env: rows for env, rows in sorted(matrix.items(), key=lambda x: x[0])}
