#!/bin/sh
# BTE V1.0 production Portal start — POSIX. Run from any cwd; chdirs to repo root.
# No --reload. Requires BTE_API_BASE_URL when API is not on 127.0.0.1:8000.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
cd "$ROOT"
PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH
HOST="${BTE_BIND_HOST:-127.0.0.1}"
PORT="${BTE_PORTAL_PORT:-8081}"
export BTE_API_BASE_URL="${BTE_API_BASE_URL:-http://127.0.0.1:8000}"
exec python -m uvicorn applications.customer_portal.app:app --host "$HOST" --port "$PORT"
