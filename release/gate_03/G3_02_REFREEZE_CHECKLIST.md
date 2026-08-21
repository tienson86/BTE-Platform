# G3-02 — Refreeze checklist

## Acceptance

| Item | Status |
|------|--------|
| Gate-1 Frozen Truth intact | **PASS** (SHA256 match; ten-case 0 diffs on proven 3.14.6 Windows) |
| Gate-2 customer semantics intact | **PASS** (no UI/narrative/export/History code changes) |
| Production topology defined | **PASS** |
| API process defined | **PASS** |
| Portal process defined | **PASS** |
| Node confirmed build-time only | **PASS** |
| Production Python version decided | **PASS — 3.14.6** |
| Clean Linux runtime validated | **FAIL** (no Docker/WSL on freeze host) |
| Required runtime data present (layout documented / Docker COPY) | **PASS** (packaging); Linux presence **unproven** |
| Playwright Chromium works on Linux | **FAIL** (not run) |
| Vietnamese PDF on Linux | **FAIL** (not run; Windows PDF OK) |
| DOCX on Linux | **FAIL** (not run; Windows DOCX OK) |
| Timezone works | **PASS** on Windows `ZoneInfo`; Linux tzdata packaged, not run |
| UTF-8 works | **PASS** on Windows JSON/DOCX; Linux locale packaged, not run |
| Startup commands frozen, no `--reload` | **PASS** |
| Health probes frozen | **PASS** |
| Restart behavior tested | **PASS** (Windows live uvicorn; not Linux) |
| Ten control cases Linux = 0 diffs | **FAIL** (not run) |
| Dũng/Tuyền PDF/DOCX parity | **PASS** on Windows; Linux **unproven** |
| Process manager recommendation documented | **PASS** |
| Resource baseline documented | **PASS** (Windows-approximate) |
| Docker status classified | **PASS** (SMOKE-ONLY) |
| No production deployment performed | **PASS** |
| Analytical semantic changes = 0 | **PASS** |
| Gate-2 semantic changes = 0 | **PASS** |

## Gate status

**G3-02: BLOCKED — PRODUCTION PROCESS/RUNTIME DEFECTS REMAIN**

Not blocked for Frozen Truth mismatch.

## Unblock for G3-03

On a Linux machine with Docker:

1. `docker compose -f deployment/docker/docker-compose.g3-02-smoke.yml up --build`
2. `docker compose -f deployment/docker/docker-compose.g3-02-smoke.yml exec api python /app/release/gate_03/_g3_02_linux_smoke.py`
3. Confirm `runtime.system` is Linux and `mismatch_count` is 0
4. Confirm Dũng/Tuyền PDF has no tofu (visual or font-list), DOCX opens
5. Only then re-issue G3-02 as PASS

Do not start G3-03 while this checklist still has Linux FAIL rows.
