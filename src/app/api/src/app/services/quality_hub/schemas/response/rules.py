"""Pydantic models for responses containing rule data."""

from pydantic import BaseModel

class RuleResponse(BaseModel):
    id: str
    project_id: str
    type: str
    threshold: float
    enabled: bool

class RuleListResponse(BaseModel):
    rules: list[RuleResponse]
