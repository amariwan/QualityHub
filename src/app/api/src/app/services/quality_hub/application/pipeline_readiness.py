from __future__ import annotations

from app.services.quality_hub.domain.value_objects.deployability import DeployabilityState


def evaluate_deployability(*, pipeline_status: str, report_summaries: list[dict]) -> dict:
    tests_failed = None
    critical_findings = None
    build_artifact_present = None
    deploy_job_failed = None

    for summary in report_summaries:
        tests_failed = summary.get("tests_failed", tests_failed)
        critical_findings = summary.get("critical_findings", critical_findings)
        build_artifact_present = summary.get("build_artifact_present", build_artifact_present)
        deploy_job_failed = summary.get("deploy_job_failed", deploy_job_failed)

    reasons: list[str] = []
    if pipeline_status.lower() in {"failed", "canceled"}:
        reasons.append("pipeline_failed")
    if tests_failed is not None and tests_failed > 0:
        reasons.append("tests_failed")
    if critical_findings is not None and critical_findings > 0:
        reasons.append("critical_findings")
    if build_artifact_present is not None and not build_artifact_present:
        reasons.append("missing_build_artifact")
    if deploy_job_failed is not None and deploy_job_failed:
        reasons.append("deploy_job_failed")

    missing = [
        name
        for name, value in {
            "tests_failed": tests_failed,
            "critical_findings": critical_findings,
            "build_artifact_present": build_artifact_present,
        }.items()
        if value is None
    ]

    if reasons:
        state = DeployabilityState.NOT_DEPLOYABLE
    elif missing:
        state = DeployabilityState.PARTIAL_UNKNOWN
    else:
        state = DeployabilityState.DEPLOYABLE

    return {
        "deployability_state": state.value,
        "failure_reasons": reasons,
        "missing_signals": missing,
    }
