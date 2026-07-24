# BTE Platform — Docker Deployment

## Prerequisites

- Docker Engine + Docker Compose v2

## Build & run

From **repository root**:

```bash
docker compose -f deployment/docker/docker-compose.yml up --build
```

Detached:

```bash
docker compose -f deployment/docker/docker-compose.yml up --build -d
```

## Services & ports

| Container | Host port | Health |
|-----------|-----------|--------|
| `bte-api` | 8000 | `/api/v1/health` |
| `bte-web-admin` | 8080 | `/healthz` |
| `bte-customer-portal` | 8081 | `/healthz` |

UI containers call the API via Docker network URL:

```text
BTE_API_BASE_URL=http://api:8000
```

## Volumes

| Host path | Container | Mode |
|-----------|-----------|------|
| `engines/` | `/app/engines` | read-only (includes knowledge) |
| `applications/data/` | `/app/applications/data` | read-write (storage) |
| `logs/` | `/app/logs` | read-write |
| `reports/` | `/app/reports` | read-write |

## Environment

Compose loads `deployment/env/production.env` and allows overrides:

```bash
BTE_STORAGE_BACKEND=sqlite BTE_LOG_LEVEL=INFO \
  docker compose -f deployment/docker/docker-compose.yml up --build
```

Template: `deployment/env/.env.example`

## Health

```bash
curl -fsS http://127.0.0.1:8000/api/v1/health
curl -fsS http://127.0.0.1:8080/healthz
curl -fsS http://127.0.0.1:8081/healthz
```

Or:

```bash
./scripts/health_check.sh
```

## Stop

```bash
docker compose -f deployment/docker/docker-compose.yml down
```

## Notes

- WP17 does **not** include Kubernetes, Nginx, or cloud automation.
- Do not commit production secrets; set `BTE_JWT_SECRET` via env / secret store.
