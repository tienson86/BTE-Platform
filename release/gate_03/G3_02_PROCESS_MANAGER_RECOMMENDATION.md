# G3-02 — Process manager recommendation

For a **single DigitalOcean Ubuntu beta host**. Recommendation only. Not implemented in this gate.

## Choice

**B. Docker Compose** (API + Portal). Optionally wrap with systemd `docker compose up` for boot/restart.

Not chosen for G3-03: **A. systemd + host venv** as the primary model.

## Why Compose

| Need | Compose | systemd + venv on Ubuntu 24.04 |
|------|---------|--------------------------------|
| Python 3.14.6 | Image pin (`python:3.14.6-slim`) | Host Python is 3.12; need deadsnakes/source build |
| Playwright OS libs | `playwright install-deps` in Dockerfile | Manual apt list, drift |
| Two FastAPI services | Two compose services, existing files | Two unit files, easy enough |
| Rollback | Retag / previous image | Re-unpack directory |
| Logs | `docker compose logs` + journald if wrapped | journald native |
| Restart | `restart: unless-stopped` | `Restart=always` |
| Reproducibility | Same image G3-02 is repairing | Depends on host packages |
| Chromium as non-root | Modeled in Dockerfile.api | Extra user + cache path work |

Repo already has compose files. After G3-02 Dockerfile repair they are the shortest path to a **Linux** 3.14.6 + Chromium runtime. systemd+venv is viable later if operations prefer fewer moving parts **after** 3.14.6 is installed on the host.

## Required manager capabilities (either model)

- start on boot
- restart on failure
- stop / restart / status
- stdout/stderr logging
- environment loading (`BTE_API_BASE_URL`, `BTE_JWT_SECRET`, `BTE_LOG_LEVEL`, `BTE_GIT_COMMIT`)

## G3-03 sketch (do not execute here)

1. Install Docker on the droplet
2. Build `Dockerfile.api` + `Dockerfile.portal` from `release/v1.0-final`
3. Run two services on an internal network; publish **only** a reverse proxy (later)
4. Run `_g3_02_linux_smoke.py` once
5. If mismatch_count ≠ 0: **STOP**

Do not open 8000/8081 on the public interface.
