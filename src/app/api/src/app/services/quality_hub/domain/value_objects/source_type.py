from enum import StrEnum


class SourceType(StrEnum):
    PUSH = "push"
    MERGE_REQUEST_EVENT = "merge_request_event"
    SCHEDULE = "schedule"
    WEB = "web"
    TRIGGER = "trigger"
