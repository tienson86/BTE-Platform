# Environment Guide

Version: 1.0.0  
Sprint: Beta-1

Three environments: **development** · **beta** · **production**.  
Templates: `deployment/docker/.env.example`, `deployment/docker/.env.production.example`.  
**No secrets in git.** `BTE_JWT_SECRET` in examples is a placeholder only.

---

## Variable catalog

| Variable | Dev default | Beta / Prod | Description |
|----------|-------------|-------------|-------------|
| `BTE_ENV` | `development` | `beta` / `production` | Environment name |
| `BTE_API_BASE_URL` | `http://127.0.0.1:8000` | `http://api:8000` (in-network) | Portal → API |
| `BTE_PUBLIC_API_PREFIX` | `/` | `/` | Public path prefix via nginx |
| `BTE_STORAGE_BACKEND` | `json` | `json` (or `sqlite`) | Persistence backend name only |
| `BTE_DATA_DIR` | `applications/data` | `/app/applications/data` | Data root |
| `BTE_LICENSE_PATH` | `applications/data/licenses.json` | volume path | License file |
| `BTE_REPORT_PATH` | `reports` | `/app/reports` | Report artifacts |
| `BTE_SQLITE_PATH` | `applications/data/bte.sqlite3` | volume path | Optional sqlite |
| `BTE_LOG_LEVEL` | `INFO` | `INFO` | Log level |
| `BTE_JWT_SECRET` | dev placeholder | **required secret** | JWT signing |
| `HOST` | `0.0.0.0` | `0.0.0.0` | Bind inside container |
| `API_PORT` | `8000` | `8000` | API listen |
| `PORTAL_PORT` | `8081` | `8081` | Portal listen |
| `NGINX_HTTP_PORT` | `80` | `80` | Ingress HTTP |
| `NGINX_HTTPS_PORT` | `443` | `443` | Ingress HTTPS |
| `TLS_CERT_PATH` | `./certs/fullchain.pem` | secret mount | Certificate (not in image) |
| `TLS_KEY_PATH` | `./certs/privkey.pem` | secret mount | Private key |
| `BTE_IMAGE_TAG` | `local` | git SHA / `1.0.0` | Image tag |
| `COMPOSE_PROFILES` | `core` | `core,edge` | Compose profiles (`core` / `edge` / `workers` / `full`) |

---

## Separation rules

1. Dev may use example JWT. Beta/prod must replace it.  
2. Compose production does not bind API to the host.  
3. Knowledge/engine trees are read-only mounts.  
4. Do not put production `.env` under the repository.

---

END
