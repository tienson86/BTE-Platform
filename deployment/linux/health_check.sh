#!/usr/bin/env bash
set -u
API_URL="${API_URL:-http://127.0.0.1:8000/api/v1/health}"
ADMIN_URL="${ADMIN_URL:-http://127.0.0.1:8080/healthz}"
PORTAL_URL="${PORTAL_URL:-http://127.0.0.1:8081/healthz}"

ok=0
check() {
  local name="$1" url="$2"
  if curl -fsS "$url" >/dev/null; then
    echo "[OK] $name  $url"
  else
    echo "[FAIL] $name  $url"
    ok=1
  fi
}

echo "Checking BTE health endpoints..."
check "API" "$API_URL"
check "Admin" "$ADMIN_URL"
check "Portal" "$PORTAL_URL"
exit "$ok"
