#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/../.." && pwd)"
cd "$ROOT"

mkdir -p logs reports applications/data "$ROOT/deployment/linux/run"

echo "========================================"
echo " BTE Platform — starting all services"
echo "========================================"

nohup bash "$DIR/start_api.sh" >/dev/null 2>&1 &
echo $! > "$ROOT/deployment/linux/run/api.pid"
sleep 2
nohup bash "$DIR/start_admin.sh" >/dev/null 2>&1 &
echo $! > "$ROOT/deployment/linux/run/admin.pid"
sleep 1
nohup bash "$DIR/start_portal.sh" >/dev/null 2>&1 &
echo $! > "$ROOT/deployment/linux/run/portal.pid"

echo
echo "Started:"
echo "  API     http://127.0.0.1:8000/docs"
echo "  Admin   http://127.0.0.1:8080"
echo "  Portal  http://127.0.0.1:8081"
echo
echo "Logs: logs/api.log , logs/admin.log , logs/portal.log"
echo "PIDs: deployment/linux/run/*.pid"
echo "Stop: deployment/linux/stop_all.sh"
