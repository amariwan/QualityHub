"""Pydantic models for incoming rule request payloads."""

from pydantic import BaseModel

class CreateRuleRequest(BaseModel):
    project_id: str
    type: str
    threshold: float
    enabled: bool = True

class PatchRuleRequest(BaseModel):
    type: str | None = None
    threshold: float | None = None
    enabled: bool | None = None
