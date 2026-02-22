from app.services.quality_hub.application.pipeline_readiness import evaluate_deployability


def test_pipeline_failed_is_not_deployable():
    result = evaluate_deployability(pipeline_status="failed", report_summaries=[])
    assert result["deployability_state"] == "not_deployable"
    assert "pipeline_failed" in result["failure_reasons"]


def test_missing_signals_is_partial_unknown():
    result = evaluate_deployability(
        pipeline_status="success",
        report_summaries=[{"build_artifact_present": True}],
    )
    assert result["deployability_state"] == "partial_unknown"


def test_summary_failures_mark_not_deployable():
    result = evaluate_deployability(
        pipeline_status="success",
        report_summaries=[
            {
                "tests_failed": 2,
                "critical_findings": 0,
                "build_artifact_present": True,
                "deploy_job_failed": False,
            }
        ],
    )
    assert result["deployability_state"] == "not_deployable"
    assert "tests_failed" in result["failure_reasons"]
