from pydantic import BaseModel


class PipelineResponse(BaseModel):
    id: int
    project_id: int
    gitlab_pipeline_id: int
    status: str
    ref: str | None
    sha: str | None
    source_type: str | None
    deployability_state: str
    failure_reasons: list[str]
    missing_signals: list[str]
