from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Cluster:
    id: int
    name: str
    kube_api: str
    kube_context_ref: str
