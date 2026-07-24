# BTE Platform — Linux Deployment

## Prerequisites

- Python 3.11+ / 3.12
- `curl` (for health checks)
- Virtualenv recommended: `.venv`

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -r applications/requirements.txt
chmod +x deployment/linux/*.sh scripts/*.sh
```

## Start all services

```bash
./deployment/linux/start_all.sh
```

Services run in background. PIDs are stored in `deployment/linux/run/*.pid`.

URLs:

- API http://127.0.0.1:8000/docs
- Admin http://127.0.0.1:8080
- Portal http://127.0.0.1:8081

## Start individually (foreground)

```bash
./deployment/linux/start_api.sh
./deployment/linux/start_admin.sh
./deployment/linux/start_portal.sh
```

## Stop

```bash
./deployment/linux/stop_all.sh
```

## Health check

```bash
./scripts/health_check.sh
# or
./deployment/linux/health_check.sh
```

## Environment

Scripts source `deployment/env/development.env` when available.

Production example:

```bash
set -a
source deployment/env/production.env
set +a
./deployment/linux/start_all.sh
```

## Logs

- `logs/api.log`
- `logs/admin.log`
- `logs/portal.log`
