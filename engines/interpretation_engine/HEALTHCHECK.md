# HEALTHCHECK.md

> Pack 03 Runtime Health

---

## Health States

| State | Meaning |
|-------|---------|
| READY | Initialized and idle |
| RUNNING | Currently executing |
| FAILED | Last execution/validation failed |
| DISABLED | Shutdown / not active |
| UNKNOWN | Not initialized / indeterminate |

## Components

- Per-runtime: `runtime.health()` via `BaseRuntime`
- Aggregate: `health/health_manager.py` → `HealthManager`

## HealthManager API

- `register` / `unregister`
- `status_map`
- `overall`
- `validate`
- `snapshot`
