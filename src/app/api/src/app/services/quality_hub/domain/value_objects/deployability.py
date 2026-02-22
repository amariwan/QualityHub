from enum import StrEnum


class DeployabilityState(StrEnum):
    DEPLOYABLE = "deployable"
    NOT_DEPLOYABLE = "not_deployable"
    PARTIAL_UNKNOWN = "partial_unknown"
