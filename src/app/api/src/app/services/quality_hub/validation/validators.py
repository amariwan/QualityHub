"""Request-level validators and coercion helpers for rules."""

from __future__ import annotations

from pydantic import BaseModel, ValidationError


class RuleValidator(BaseModel):
    project_id: str
    type: str
    threshold: float
    enabled: bool = True


def validate_create(data: dict) -> RuleValidator:
    return RuleValidator(**data)
