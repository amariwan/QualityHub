from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Report:
    id: int
    pipeline_id: int
    type: str
    summary_json: dict
