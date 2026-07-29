# BTE Platform — Deployment Overview (WP17)

This layer packages **how to run** BTE in production-like environments.
It does **not** change engines, knowledge, or application business code.

## Services

| Service | Module | Default port | Health |
|---------|--------|--------------|--------|
| API | `applications.api.app:app` | 8000 | `GET /api/v1/health` |
| Web Admin | `applications.web_admin.app:app` | 8080 | `GET /healthz` |
| Customer Portal | `applications.customer_portal.app:app` | 8081 | `GET /healthz` |

## Environment variables

See `deployment/env/.env.example`.

| Variable | Purpose |
|----------|---------|
| `BTE_API_BASE_URL` | UI → API base URL |
| `BTE_STORAGE_BACKEND` | `json` \| `sqlite` \| `postgres` |
| `BTE_LICENSE_PATH` | License JSON path |
| `BTE_REPORT_PATH` | Report export directory |
| `BTE_LOG_LEVEL` | Logging level |
| `HOST` | Bind host |
| `PORT` | Bind port (per process) |

Also used by local scripts: `API_PORT`, `ADMIN_PORT`, `PORTAL_PORT`, `BTE_DATA_DIR`, `BTE_JWT_SECRET`.

## Quick start

### Windows

```bat
deployment\windows\start_all.bat
scripts\health_check.bat
```

### Linux

```bash
chmod +x deployment/linux/*.sh scripts/*.sh
./deployment/linux/start_all.sh
./scripts/health_check.sh
```

### Docker

```bash
docker compose -f deployment/docker/docker-compose.yml up --build
```

## Logs

Runtime logs are written under `logs/`:

- `logs/api.log`
- `logs/admin.log`
- `logs/portal.log`

## Volumes (Docker)

- `engines/` (read-only) — includes knowledge bases
- `applications/data/` — JSON/SQLite application storage
- `logs/`
- `reports/`

## Docs

- [WINDOWS.md](WINDOWS.md)
- [LINUX.md](LINUX.md)
- [DOCKER.md](DOCKER.md)

## Out of scope (WP17)

Kubernetes, Nginx, cloud provisioning, new databases, business-logic changes.
