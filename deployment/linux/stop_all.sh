#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RUN_DIR="$ROOT/deployment/linux/run"

echo "Stopping BTE services..."

stop_pidfile() {
  local name="$1"
  local file="$RUN_DIR/$name.pid"
  if [[ -f "$file" ]]; then
    local pid
    pid="$(cat "$file" || true)"
    if [[ -n "${pid}" ]] && kill -0 "$pid" 2>/dev/null; then
      # Kill process group / children started via nohup bash
      pkill -P "$pid" 2>/dev/null || true
      kill "$pid" 2>/dev/null || true
      echo "Stopped $name (pid $pid)"
    fi
    rm -f "$file"
  fi
}

stop_pidfile api
stop_pidfile admin
stop_pidfile portal

# Fallback: match uvicorn command lines
pkill -f "uvicorn applications.api.app:app" 2>/dev/null || true
pkill -f "uvicorn applications.web_admin.app:app" 2>/dev/null || true
pkill -f "uvicorn applications.customer_portal.app:app" 2>/dev/null || true

echo "Done."
