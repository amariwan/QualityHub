from pydantic import BaseModel


class ReportUploadMetadata(BaseModel):
    pipeline_id: int
    type: str
