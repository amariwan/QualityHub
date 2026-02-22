from __future__ import annotations

from app.services.quality_hub.application.pipeline_readiness import evaluate_deployability
from app.services.quality_hub.infrastructure.repositories import QualityHubRepository


async def list_broken_pipelines(repository: QualityHubRepository, scope: str = "all") -> list[dict]:
    rows = await repository.list_pipelines()
    data: list[dict] = []
    for row in rows:
        reports = await repository.list_reports_for_pipeline(row.id)
        readiness = evaluate_deployability(
            pipeline_status=row.status,
            report_summaries=[report.summary_json for report in reports],
        )
        if scope == "readiness":
            if not (
                (row.ref and row.ref.startswith("release/")) or row.source_type in {"push", "merge_request_event", "schedule"}
            ):
                continue
        if readiness["deployability_state"] == "deployable":
            continue
        data.append(
            {
                "id": row.id,
                "project_id": row.project_id,
                "gitlab_pipeline_id": row.gitlab_pipeline_id,
                "status": row.status,
                "ref": row.ref,
                "sha": row.sha,
                "source_type": row.source_type,
                **readiness,
            }
        )
    return data
