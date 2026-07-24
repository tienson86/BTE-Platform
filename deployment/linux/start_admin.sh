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
export PORT="${ADMIN_PORT:-8080}"
export BTE_API_BASE_URL="${BTE_API_BASE_URL:-http://127.0.0.1:8000}"
export BTE_LOG_LEVEL="${BTE_LOG_LEVEL:-INFO}"

PYTHON="python3"
[[ -x .venv/bin/python ]] && PYTHON=".venv/bin/python"

echo "Starting BTE Web Admin on ${HOST}:${PORT} ..."
exec "$PYTHON" -m uvicorn applications.web_admin.app:app --host "$HOST" --port "$PORT" \
  >> logs/admin.log 2>&1
