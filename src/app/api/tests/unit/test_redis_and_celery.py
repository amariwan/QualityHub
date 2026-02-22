from importlib import reload

import pytest


def test_redis_settings_and_client(monkeypatch):
    # without URL, settings should still initialise to None and client errors
    monkeypatch.delenv("REDIS_URL", raising=False)
    from app.config import get_redis_settings

    settings = get_redis_settings()
    assert settings.REDIS_URL is None

    # building client without URL should raise
    from app.core.core_tasks.redis_client import get_redis_client

    with pytest.raises(RuntimeError):
        get_redis_client()

    # when URL is set we should be able to construct a client instance
    monkeypatch.setenv("REDIS_URL", "redis://example:6379/2")
    reload(get_redis_settings.__module__)
    reload(get_redis_client.__module__)

    settings = get_redis_settings()
    assert settings.REDIS_URL == "redis://example:6379/2"

    client = get_redis_client()
    from redis.asyncio import Redis

    assert isinstance(client, Redis)
    # the ``connection_pool`` object must have parsed the URL correctly
    assert "/2" in client.connection_pool.connection_kwargs.get("db", "")


def test_celery_settings_and_app(monkeypatch):
    # if no broker url is provided, celery_app should fall back to in-memory
    monkeypatch.delenv("CELERY_BROKER_URL", raising=False)
    monkeypatch.delenv("CELERY_RESULT_BACKEND", raising=False)

    # reload modules to pick up environment changes
    import app.core.core_tasks.celery_app as celery_mod
    reload(celery_mod)

    celery = celery_mod.celery
    assert celery.conf.broker_url == "memory://"
    # rpc backend is the default when broker is memory
    assert celery.conf.result_backend == "rpc://"

    # setting explicit URLs should be respected
    monkeypatch.setenv("CELERY_BROKER_URL", "redis://foo:6379/3")
    monkeypatch.setenv("CELERY_RESULT_BACKEND", "redis://foo:6379/4")
    reload(celery_mod)
    celery = celery_mod.celery
    assert celery.conf.broker_url == "redis://foo:6379/3"
    assert celery.conf.result_backend == "redis://foo:6379/4"


def test_example_celery_task(monkeypatch):
    # make sure the task can be imported and executed with memory broker
    monkeypatch.setenv("CELERY_BROKER_URL", "")
    monkeypatch.setenv("CELERY_RESULT_BACKEND", "")
    # re-import tasks to ensure they bind to the new app instance
    import app.core.core_tasks.celery_app as celery_mod
    import app.core.core_tasks.tasks as tasks_mod
    reload(celery_mod)
    reload(tasks_mod)

    result = tasks_mod.add.delay(3, 4)
    assert result.get(timeout=1) == 7
