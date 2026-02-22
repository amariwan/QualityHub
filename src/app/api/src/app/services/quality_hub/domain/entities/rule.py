"""Domain entity representing a quality rule."""

from __future__ import annotations

from dataclasses import dataclass

from ..value_objects.threshold import Threshold
from ..value_objects.rule_type import RuleType

@dataclass
class Rule:
    id: str
    project_id: str
    type: RuleType
    threshold: Threshold
    enabled: bool = True
