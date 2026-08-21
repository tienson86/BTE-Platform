# G3-02 — Production process freeze report

**Status: G3-02: BLOCKED — PRODUCTION PROCESS/RUNTIME DEFECTS REMAIN**

Date: 2026-08-21  
Branch: `release/v1.0-final`  
HEAD: `2d83ee3e209051ab840c17f6aad8ae4fd3ba017b` (same as G3-01 / G2-FINAL)

Do not start G3-03 automatically.

## 1. Entry baseline

| Item | Result |
|------|--------|
| Expected freeze HEAD | `2d83ee3e` |
| Recorded HEAD | `2d83ee3e209051ab840c17f6aad8ae4fd3ba017b` |
| Gate-1 101 SHA256 | `46386BC955119F5DFE9482E7D620767BFB8BB74003A0968A17A6F82017FFA5CC` — match |
| G2-FINAL artifacts | present under `release/gate_02/` |
| G3-01 manifests | present under `release/gate_03/` |
| Working tree vs HEAD | uncommitted G2-FINAL / G3-01 / G3-02 packaging + docs (no engine semantic edits) |

HEAD did not move from G3-01. Delta is documentation and runtime packaging only.

## 2. What this gate answered

| Question | Answer |
|----------|--------|
| Which processes? | **A:** Applications API. **B:** Customer Portal. No Node process. No worker. |
| Ports | API **8000**. Portal **8081**. |
| Portal → API | `GET/POST /backend/{path}` → `BTE_API_BASE_URL` (default `http://127.0.0.1:8000`), timeout **120 s** |
| Start/stop | POSIX `deployment/process/start-api.sh` / `start-portal.sh`; no `--reload` |
| Health | API `GET /health`, `GET /version`, `GET /api/v1/health`. Portal `GET /healthz` |
| Linux/Python | **Production Python = CPython 3.14.6.** Linux container smoke **not executed** on this host (no Docker, no WSL). |
| Later package | engines, applications (no `node_modules`/`src`), `database/`, knowledge runtime subset, Playwright Chromium, fonts, tzdata |

## 3. Absolute freeze

| Layer | This gate |
|-------|-----------|
| Gate-1 analytical engines/rules | **0** semantic changes |
| Gate-2 customer semantics | **0** semantic changes |
| Ten-case probe (this host, CPython 3.14.6 Windows) | **0 diffs** (`release/gate_03/G3_02_SMOKE.json`) |
| Production deployment (droplet/DNS/TLS/firewall/GitHub Release) | **not performed** |

Allowed application change: `applications/api/config.py` reads `BTE_LOG_LEVEL` (ops logging only).

## 4. Why BLOCKED

Acceptance requires a **clean Linux runtime** with ten control cases = 0 diffs, Playwright Chromium on Linux, and Vietnamese PDF/DOCX generated **inside that Linux environment**.

This freeze host:

- Docker is not installed
- WSL is not installed
- Python 3.12 is not installed

Therefore the Linux probe was **not executed**. Process topology, Python version, health contract, and Docker packaging are defined, but G3-02 cannot PASS until the same smoke is run on Linux.

This is **not** a Frozen Truth mismatch. Windows 3.14.6 ten-case + Dũng/Tuyền PDF/DOCX remain MATCH.

## 5. Production Python

**CPython 3.14.6**

Python 3.12 is **not approved**. pandas 3.0.5 has Linux cp312 wheels, but Frozen Truth has never been reproduced on 3.12. Do not rewrite engines to chase 3.12. Details: `G3_02_PYTHON_BASELINE_DECISION.md`.

## 6. Topology (frozen intent)

```
Internet
  → future reverse proxy (G3-03/G3-04; not this gate)
      → Portal :8081  (public via proxy only)
          → /backend/*  → API :8000  (internal)
              → engines + database/ + knowledge runtime
              → official PDF/DOCX inside the API process (Playwright / python-docx)
```

History is browser-local. No customer History database.

## 7. Changed files (packaging / ops)

| File | Role |
|------|------|
| `applications/api/config.py` | Read `BTE_LOG_LEVEL` |
| `deployment/docker/Dockerfile.api` | 3.14.6, `database/`, knowledge subset, Playwright, fonts, tzdata, non-root |
| `deployment/docker/Dockerfile.portal` | 3.14.6, non-root, `requirements-prod.txt` |
| `deployment/docker/Dockerfile.customer_portal` | Same as portal (compose alias) |
| `deployment/docker/.dockerignore` | Keep knowledge markdown catalogs; drop Portal `src` |
| `deployment/docker/docker-compose.g3-02-smoke.yml` | Loopback smoke compose |
| `deployment/process/start-api.sh` | POSIX API start, default `127.0.0.1` |
| `deployment/process/start-portal.sh` | POSIX Portal start |
| `release/gate_03/_g3_02_linux_smoke.py` | Release smoke (not a healthcheck) |
| `release/gate_03/_g3_02_linux_smoke.sh` | Linux wrapper + `pip check` |
| `release/gate_03/_g3_02_process_restart.py` | Live API restart probe |

## 8. Tests executed

| Probe | Result |
|-------|--------|
| `python release/gate_03/_g3_02_linux_smoke.py` | **PASS** on Windows 3.14.6; mismatch_count **0**; Dũng/Tuyền PDF `%PDF-` + DOCX zip |
| `python release/gate_03/_g3_02_process_restart.py` | **PASS** — Dũng Dụng unchanged across SIGTERM restart |
| Linux Docker compose smoke | **NOT RUN** |
| Full pytest | not run (module-only rule) |

## 9. Remaining failures

1. Linux ten-case probe not executed
2. Linux Playwright/fonts/PDF tofu check not executed
3. Docker images not built on this host → classified **SMOKE-ONLY**
4. `GET /version` still has only contract fields (tests freeze exact keys); set `BTE_GIT_COMMIT` in the process environment at deploy time
5. Unhandled API 500 still returns `str(exc)` to the client (traceback is server-logged). Do not treat this as Gate-2 copy; G3-05 may hide it.

## 10. Final status

**G3-02: BLOCKED — PRODUCTION PROCESS/RUNTIME DEFECTS REMAIN**

Re-run on a Linux host with Docker (compose bind-mounts `release/` into the API container):

```
docker compose -f deployment/docker/docker-compose.g3-02-smoke.yml up --build
docker compose -f deployment/docker/docker-compose.g3-02-smoke.yml exec api python /app/release/gate_03/_g3_02_linux_smoke.py
```

Until Linux mismatch_count is 0, do not start G3-03.
