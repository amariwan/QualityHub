from enum import StrEnum


class ScopeType(StrEnum):
    PROJECT = "PROJECT"
    PROJECT_ENV = "PROJECT_ENV"
    PROJECT_ENV_CLUSTER = "PROJECT_ENV_CLUSTER"
