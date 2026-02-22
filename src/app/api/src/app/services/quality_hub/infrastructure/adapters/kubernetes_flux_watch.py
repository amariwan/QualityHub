from __future__ import annotations

import time
from collections.abc import Iterator


class KubernetesFluxWatchAdapter:
    """Best-effort watch adapter skeleton for HelmRelease and Kustomization events.

    The implementation yields no-op heartbeat events when cluster access is not configured.
    Extend this adapter to call Kubernetes watch APIs in production.
    """

    def stream_flux_events(self, cluster: dict) -> Iterator[dict]:
        cluster_id = cluster.get("id")
        while True:
            yield {
                "kind": "heartbeat",
                "cluster_id": cluster_id,
                "status": "unknown",
                "message": "watch heartbeat",
            }
            time.sleep(15)
