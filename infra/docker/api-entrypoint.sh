#!/usr/bin/env bash
set -euo pipefail

cd /app/src/app/api
alembic upgrade head
uvicorn app.asgi:app --host 0.0.0.0 --port 8000
