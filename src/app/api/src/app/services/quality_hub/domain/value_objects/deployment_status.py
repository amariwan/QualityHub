from enum import StrEnum


class DeploymentStatus(StrEnum):
    READY = "ready"
    PROGRESSING = "progressing"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"
