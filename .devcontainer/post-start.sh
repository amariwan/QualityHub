#!/usr/bin/env bash
set -euo pipefail

sudo chown -R "$(id -u):$(id -g)" /home/developer/.npm 2>/dev/null || true
sudo chown -R "$(id -u):$(id -g)" /home/developer/.cache 2>/dev/null || true

cat <<'MSG'
[devcontainer] Ready.
Quick start:
  pnpm dev
  cd src/app/api && uv run uvicorn app.asgi:app --host 0.0.0.0 --port 8000 --reload
MSG
