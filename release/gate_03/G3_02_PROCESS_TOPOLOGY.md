# G3-02 — Process topology

Frozen intent for BTE V1.0. Not a live production deployment.

## Processes

| Process | Role | Entry | Bind | Public? |
|---------|------|-------|------|---------|
| **A — BTE API** | Analyze, narrative, official PDF/DOCX | `applications.api.app:app` | internal **8000** | No |
| **B — Customer Portal** | FastAPI static UI + `/backend` proxy | `applications.customer_portal.app:app` | internal **8081** | Only via future reverse proxy |

Node.js is **build-time only** (`npm ci` + `npm run build:result`). Production Portal serves `applications/customer_portal/static/` including `static/dist/`.

No additional V1.0 process for:

- Playwright PDF — inside API (`PdfExporterV1`, sync Chromium launch/close)
- DOCX — inside API (`DocxExporterV1`)
- background jobs / scheduler / worker — `Dockerfile.worker` is reserved stub, **not required**
- web admin — **not** in the V1.0 customer topology

## Customer path

```
Customer browser
  → future reverse proxy / edge          (G3-03/G4 — TLS, hostname)
      → Portal service :8081
          HTML /static/*  (same origin)
          /backend/{path}  → http://{BTE_API_BASE_URL}/{path}
              → API service :8000
                  engines + database/ + knowledge runtime
                  PDF/DOCX in-process → temp file → download → delete
```

## Direct internal API use

Official export is **not** a third process. Portal `POST /backend/api/v1/export/pdf` and `/export/docx` forward the selected ResultStore payload to the API. Report HTML is rendered in the API; Chromium runs in the API process.

There is **no** customer History database. History is browser-local (max 30).

## `/backend` proxy (live code)

Source: `applications/customer_portal/app.py`

| Item | Value |
|------|--------|
| Target | `{BTE_API_BASE_URL}/{path}` |
| Default URL | `http://127.0.0.1:8000` (same host; **configurable**) |
| Compose/Docker | `http://api:8000` |
| Timeout | `httpx.AsyncClient(timeout=120.0)` |
| Headers | forwarded except hop-by-hop (`host`, `content-length`, `connection`, …) |
| Identity | client may send `X-Request-ID`; API middleware copies or mints UUID. Frozen JS `api.js` does not set it; API generates the id that becomes `analysis_id`. |
| Body | raw request body (Analyze JSON). Not logged by API access middleware. |
| Errors | connect failures currently surface as unhandled 500 (httpx). Healthz does **not** require API. |

`localhost` is the **same-host** default, not a developer-only hard-code that blocks Linux. Override with `BTE_API_BASE_URL`.

Vite `src/config/api.ts` browser default is `/backend/api/v1` (same origin). Dev `127.0.0.1:8000` is non-browser fallback only.

## Port policy

| Audience | Bind |
|----------|------|
| systemd on a host behind nginx | `127.0.0.1:8000` and `127.0.0.1:8081` (`BTE_BIND_HOST`) |
| Docker bridge | container `0.0.0.0` on the compose network; **do not** publish 8000/8081 to the public internet |
| G3-02 smoke compose | `127.0.0.1:8000:8000` and `127.0.0.1:8081:8081` (loopback only) |

Firewall/public DNS is later Gate 3. Desired freeze: public **reverse proxy only**.

## Start / stop

Working directory: **repository root** (or `/app` in the image). Engines resolve `database/` and `knowledge/` from `__file__` relative to that layout.

```
# API — no --reload
python -m uvicorn applications.api.app:app --host 127.0.0.1 --port 8000

# Portal — no --reload
python -m uvicorn applications.customer_portal.app:app --host 127.0.0.1 --port 8081
```

POSIX wrappers: `deployment/process/start-api.sh`, `start-portal.sh`.

Start order: **independent**. Recommended: API first, then Portal. Portal starts without API; `/backend` fails until API is up. Health probes detect each process separately.

Workers: **1** uvicorn worker (default). Do not raise workers: Playwright is in-process and ResultStore is browser-local, but export temp files and Chromium memory are process-local.

## Environment mode

There is no application-wide `development|production|testing` switch that changes Analyze truth.

| Concern | Production freeze |
|---------|-------------------|
| `--reload` | forbidden |
| Vite dev server | forbidden (build-time only) |
| Mock preview | `resolveDataSource` is `api` in browser; mock is test-only |
| CORS | Applications API has **no** CORSMiddleware. Consoles with `allow_origins=["*"]` are **not** customer production. |
| `/docs` | still mounted on API; reverse proxy must not publish it |

`BTE_ENV` appears in older compose files and is **unused** by Applications API code.
