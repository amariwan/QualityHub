from __future__ import annotations

from celery import Celery

from app.config import get_celery_settings

settings = get_celery_settings()

broker_url = settings.CELERY_BROKER_URL or ""
result_backend = settings.CELERY_RESULT_BACKEND or broker_url

# fallback for local development / testing if no broker is configured
if not broker_url:
    # celery memory transport has several caveats but is sufficient for
    # basic unit tests and local experimentation.
    broker_url = "memory://"
    # ``rpc://`` uses ``kombu``'s in-memory transport by default and
    # works with ``AsyncResult.get`` when the broker is memory.  it's
    # not persisted across processes so it should only be used in tests
    # or debug scenarios.
    result_backend = "rpc://"

celery: Celery = Celery("app", broker=broker_url, backend=result_backend)
# sensible defaults for our service
celery.conf.task_track_started = True


# allow tasks to be discovered using the usual celery autodiscover
# mechanism; modules under ``app.core.core_tasks`` should be named
# ``tasks.py``
celery.autodiscover_tasks(["app.core.core_tasks"])
