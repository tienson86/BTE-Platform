# Healthcheck Specification

Version: 1.0.0  
Sprint: Beta-1  
**Deployment contracts only. No new application routes in this sprint.**

---

## Logical probes

| Name | Intent | Beta-1 mapping |
|------|--------|----------------|
| `/live` | Process up | API `GET /health` → `{ "status": "ok" }`; Portal `GET /healthz` |
| `/ready` | Accept traffic | Same mapping until a dedicated ready route is product-approved |
| `/health` | Aggregate liveness | API `GET /health` and `GET /api/v1/health` |
| `/version` | Build/contract identity | API `GET /version` (`api_version`, `schema_version`, `minimum_engine_version`) |

Nginx may expose `/live` and `/ready` as **proxy_pass** aliases to the mappings above (config only).

## Compose

```
healthcheck.test: curl -fsS http://127.0.0.1:8000/health
```

Unhealthy → restart policy `unless-stopped` (dev/beta) / `always` (production).

## Success criteria

HTTP 200 + JSON body without stack traces.  
`/version` must match the released contract versions — do not change the endpoint schema here.

---

END
