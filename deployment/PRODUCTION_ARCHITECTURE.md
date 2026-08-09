# Production Architecture

Version: 1.0.0  
Sprint: Beta-1  
AF-1: **unchanged**

---

## Runtime topology

```
Client
  ↓  HTTPS (443)
Nginx (reverse proxy)
  ├─ /           → portal:8081
  ├─ /static     → portal (cache)
  └─ /api /health /version /analysis → api:8000
       ↓
Applications API
  ↓  Engine public APIs only
Engines (read-only knowledge + data volumes)
```

Worker service is **reserved** (no jobs in Beta-1).

---

## Networks

| Network | Members | Purpose |
|---------|---------|---------|
| `bte-edge` | nginx | Public ingress |
| `bte-app` | nginx, portal, api | East-west HTTP |
| `bte-data` | api, worker (reserved) | Data plane |

API is not published on the host in production compose (nginx only).

---

## Volumes

| Volume | Content |
|--------|---------|
| `bte-data` | Application JSON / license / sqlite path |
| `bte-logs` | Application + access logs |
| `bte-reports` | Generated report artifacts |
| Engine bind (ro) | `engines/` knowledge — read only |

---

## Health contracts (existing app endpoints)

| Probe | Maps to (no new routes in Beta-1) |
|-------|-----------------------------------|
| `/live` | API `GET /health` · Portal `GET /healthz` |
| `/ready` | Same until a dedicated ready route exists |
| `/health` | API `GET /health` and `GET /api/v1/health` |
| `/version` | API `GET /version` |

See [HEALTHCHECK_SPEC.md](./HEALTHCHECK_SPEC.md).

---

## What this does not change

Engines · pipelines · API contracts · Knowledge content · Foundation · Product UI · AF-1 module boundaries.

---

END
