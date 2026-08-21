#!/bin/sh
# BTE V1.0 production API start — POSIX. Run from any cwd; chdirs to repo root.
# No --reload. Default bind is loopback for a later reverse proxy.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname "$0")/../.." && pwd)
cd "$ROOT"
PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH
HOST="${BTE_BIND_HOST:-127.0.0.1}"
PORT="${BTE_API_PORT:-8000}"
exec python -m uvicorn applications.api.app:app --host "$HOST" --port "$PORT"
