from __future__ import annotations

from urllib.parse import urlparse


def parse_group_reference(group_url: str) -> str:
    parsed = urlparse(group_url)
    path = parsed.path.strip("/")
    if not path:
        raise ValueError("Invalid group URL")
    return path
