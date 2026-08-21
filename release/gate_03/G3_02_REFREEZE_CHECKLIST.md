# G3-02 — Refreeze checklist

## Acceptance

| Item | Status |
|------|--------|
| Gate-1 Frozen Truth intact | **PASS** (SHA256 match; ten-case 0 diffs on proven 3.14.6 Windows **and** Linux container) |
| Gate-2 customer semantics intact | **PASS** (no UI/narrative/export/History code changes) |
| Production topology defined | **PASS** |
| API process defined | **PASS** |
| Portal process defined | **PASS** |
| Node confirmed build-time only | **PASS** |
| Production Python version decided | **PASS — 3.14.6** |
| Clean Linux runtime validated | **PASS** (`bte-api:g3-02-smoke`, G3-02L-R1) |
| Required runtime data present (layout documented / Docker COPY) | **PASS** including `knowledge/interpretation/knowledge_registry.json` |
| Playwright Chromium works on Linux | **PASS** (Dũng/Tuyền PDF `%PDF-`) |
| Vietnamese PDF on Linux | **PASS** (PDF generated; DOCX Vietnamese + Hỷ checks) |
| DOCX on Linux | **PASS** (zip; Hỷ; Đ/ă/â) |
| Timezone works | **PASS** (`ZoneInfo("Asia/Ho_Chi_Minh")` in Linux image) |
| UTF-8 works | **PASS** (`LANG=C.UTF-8`, JSON/DOCX) |
| Startup commands frozen, no `--reload` | **PASS** |
| Health probes frozen | **PASS** |
| Restart behavior tested | **PASS** (Windows live uvicorn; Linux compose recreate/rebuild) |
| Ten control cases Linux = 0 diffs | **PASS** |
| Dũng/Tuyền PDF/DOCX parity | **PASS** on Windows and Linux smoke |
| Process manager recommendation documented | **PASS** |
| Resource baseline documented | **PASS** (Windows-approximate; Linux smoke elapsed recorded in `G3_02_SMOKE.json`) |
| Docker status classified | **PASS** (smoke compose still loopback-only) |
| No production deployment performed | **PASS** |
| Analytical semantic changes = 0 | **PASS** |
| Gate-2 semantic changes = 0 | **PASS** |

## Gate status

**G3-02: PRODUCTION PROCESS MODEL FROZEN — READY FOR G3-03**

Packaging repair: `release/gate_03/G3_02L_R1_RUNTIME_KNOWLEDGE_PACKAGING_REPAIR.md`.

Do not start G3-03 automatically from this checklist update.

## Unblock for G3-03 (completed on Linux Docker host)

1. `docker compose -f deployment/docker/docker-compose.g3-02-smoke.yml up --build` — done (`--no-cache` rebuild after R1)
2. `docker compose -f deployment/docker/docker-compose.g3-02-smoke.yml exec api python /app/release/gate_03/_g3_02_linux_smoke.py` — done
3. `runtime.system` is Linux and `mismatch_count` is 0 — confirmed
4. Dũng/Tuyền PDF `%PDF-`, DOCX opens (zip + Vietnamese/Hỷ) — confirmed
5. Re-issue G3-02 as PASS — this document
