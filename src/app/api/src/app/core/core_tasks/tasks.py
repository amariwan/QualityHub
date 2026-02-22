from __future__ import annotations

from app.core.core_tasks.celery_app import celery


@celery.task(name="app.tasks.add")
def add(x: int, y: int) -> int:
    """Example task used by tests.

    Celery serialises the return value so the signature should use
    primitive types only.  More realistic workers live elsewhere in
    the repository and can import helper modules from ``app``.
    """
    return x + y
