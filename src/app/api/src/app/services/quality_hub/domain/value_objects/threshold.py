"""Typed threshold with validation."""

from __future__ import annotations

from pydantic import BaseModel, validator

class Threshold(BaseModel):
    value: float

    @validator("value")
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("threshold must be non-negative")
        return v
