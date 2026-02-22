#!/usr/bin/env bash
set -euo pipefail

cd /app/src/app/api
celery -A app.core.tasks.beat_schedule.celery_app beat -l info
