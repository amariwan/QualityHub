#!/usr/bin/env bash
set -euo pipefail

cd /app/src/app/api
celery -A app.core.tasks.celery_app.celery_app worker -l info
