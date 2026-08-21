# G3-01 — Environment variables

V1.0 customer runtime. Placeholders only. Template: `.env.example` (also `deployment/env/.env.example`).

| Variable | Component | Required? | Default | Secret? | If missing |
|----------|-----------|-----------|---------|---------|------------|
| `BTE_API_BASE_URL` | Portal proxy | Yes in split deploy | `http://127.0.0.1:8000` | No | Proxy to wrong host / connection errors |
| `BTE_JWT_SECRET` | API JWT | Production yes | code default `bte-dev-jwt-secret-change-me` | Yes | Weak default; **must change** |
| `BTE_DATA_DIR` | WP11 JSON store | No for Analyze | `applications/data` | No | Uses repo-relative data dir |
| `BTE_STORAGE_BACKEND` | storage factory | No | `json` | No | json |
| `BTE_SQLITE_PATH` | storage | Only if sqlite | none | Path | unused if json |
| `BTE_POSTGRES_DSN` | storage | Only if postgres | none | Yes | unused if json |
| `HOST` | uvicorn bind | Ops | CLI `--host` | No | 127.0.0.1 if CLI default |
| `PORT` | API uvicorn | Ops | CLI `--port 8000` | No | 8000 |
| `PORTAL_PORT` | docs / compose | Ops | 8081 | No | not read by PortalSettings.port (code 8081) |
| `BTE_LOG_LEVEL` | Docker template | No | — | No | **Not read** by Applications API |
| `BTE_ANALYSIS_AUTH_REQUIRED` | analysis_engine API | No | `0` | No | unused on customer `/api/v1/analyze` |
| `VITE_API_BASE_URL` | Portal **build** | Build-time | `/backend/api/v1` | No | baked into `result.js` |
| `VITE_DATA_SOURCE` | Portal **build** | Build-time | `api` | No | must be `api` for production |

Customer Analyze timezone is the **request field** (default `Asia/Ho_Chi_Minh` in API settings). Server OS timezone is not the calendar authority.

## Ports

| Port | Role | Class |
|------|------|--------|
| 8000 | Applications API | PRODUCTION |
| 8081 | Customer Portal FastAPI | PRODUCTION |
| 8080 | Web admin | not V1.0 customer |
| Vite dev | `dev:result` watch | DEVELOPMENT — do not expose |

Production Portal is FastAPI static + HTML, proxy `/backend/*` → API. Not a Node server.

## Secrets

Tracked scan for tokens/keys: **none found**. Do not commit filled `.env`. Docker compose example JWT is a **dev placeholder**, not a production secret.
