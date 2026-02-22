from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol


class KubeWatchClientPort(Protocol):
    def stream_flux_events(self, cluster: dict) -> Iterator[dict]: ...
