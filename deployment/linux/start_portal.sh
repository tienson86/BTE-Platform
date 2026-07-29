#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

mkdir -p logs

set -a
# shellcheck disable=SC1091
[[ -f deployment/env/development.env ]] && . deployment/env/development.env
set +a

export HOST="${HOST:-127.0.0.1}"
export PORT="${PORTAL_PORT:-8081}"
export BTE_API_BASE_URL="${BTE_API_BASE_URL:-http://127.0.0.1:8000}"
export BTE_LOG_LEVEL="${BTE_LOG_LEVEL:-INFO}"

PYTHON="python3"
[[ -x .venv/bin/python ]] && PYTHON=".venv/bin/python"

echo "Starting BTE Customer Portal on ${HOST}:${PORT} ..."
exec "$PYTHON" -m uvicorn applications.customer_portal.app:app --host "$HOST" --port "$PORT" \
  >> logs/portal.log 2>&1
