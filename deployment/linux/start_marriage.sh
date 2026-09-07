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
export PORT="${BTE_MARRIAGE_PORT:-8082}"
export BTE_LOG_LEVEL="${BTE_LOG_LEVEL:-INFO}"

PYTHON="python3"
[[ -x .venv/bin/python ]] && PYTHON=".venv/bin/python"

echo "Starting BTE Marriage Public API on ${HOST}:${PORT} ..."
exec "$PYTHON" -m uvicorn consulting.marriage.api.http:create_marriage_api_app --factory \
  --host "$HOST" --port "$PORT" \
  >> logs/marriage_api.log 2>&1
