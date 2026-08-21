# G3-01 — Runtime & dependency freeze report

**Status: G3-01: RUNTIME & DEPENDENCY FROZEN — READY FOR G3-02**

Date: 2026-08-21  
Branch: `release/v1.0-final`  
HEAD: `2d83ee3e209051ab840c17f6aad8ae4fd3ba017b` (matches G2-FINAL)

Working tree at entry: **not unknown-dirty production**. Uncommitted files were G2-FINAL freeze documentation only. G3-01 did not change Gate-1 engines or Gate-2 customer semantics.

## Can V1.0 be reproduced?

Yes, from a git checkout of this freeze plus documented commands:

1. Python 3.14.6 (proven) + `pip install -r requirements-prod.txt -c constraints-v1.0.txt`
2. `python -m playwright install chromium`
3. Node 24.18.0 / npm 11.16.0 + `npm ci` then `npm run build:result` in `applications/customer_portal`
4. Start API + Portal with uvicorn **without** `--reload`
5. Run `python release/gate_03/_g3_01_runtime_smoke.py`

Clean-venv smoke: **PASS**, ten-case analytical **mismatch_count 0**, official PDF/DOCX for Dũng generated without developer-only paths.

## Runtime component inventory

| Component | Technology | Runtime or build? | Entry point | Manifest | Prod? | Generated? | Version-sensitive? |
|-----------|------------|-------------------|-------------|----------|-------|------------|-------------------|
| Applications API | FastAPI / uvicorn | Runtime | `applications.api.app:app` | `requirements-prod.txt` | Yes | No | Yes |
| Customer Portal | FastAPI + static | Runtime | `applications.customer_portal.app:app` | same Python + Portal static | Yes | Serves dist | Yes |
| Result bundle | Vite / React | Build | `npm run build:result` | `package-lock.json` | Yes (artifact) | `static/dist/` | Yes |
| Official PDF | Playwright Chromium | Runtime | `PdfExporterV1` | playwright 1.62.0 | Yes | Temp files | Yes |
| Official DOCX | python-docx | Runtime | `DocxExporterV1` | python-docx 1.2.0 | Yes | Temp files | Yes |
| Calendar / rules | CSV/JSON | Runtime | `__file__` → `database/`, engine data | git tree | Yes | No | Frozen Gate 1 |
| Knowledge CSVs | CSV | Runtime | `database/20_knowledge/` | git tree | Yes | No | Frozen |
| ResultStore | browser localStorage | Runtime | Portal JS | none (client) | Yes | No | G2-05 freeze |
| Playwright browsers | Chromium | Runtime | `playwright install chromium` | not in git | Yes | Local cache | Yes |
| Node | npm ci | Build only | n/a | lockfile | No (not a prod process) | n/a | Yes |

## Freeze baseline

| Item | Result |
|------|--------|
| Gate-1 101 SHA256 | `46386BC955119F5DFE9482E7D620767BFB8BB74003A0968A17A6F82017FFA5CC` — match |
| G2-FINAL artifacts | present under `release/gate_02/` |
| Analytical engine/rule files this gate | **0** |
| Gate-2 customer semantic files this gate | **0** |

## Allowed G3-01 artifacts

| File | Role |
|------|------|
| `requirements-prod.txt` | Canonical production direct pins |
| `constraints-v1.0.txt` | Clean-venv full pin set |
| `.env.example` | Placeholders only |
| `release/gate_03/_g3_01_runtime_smoke.py` | Clean runtime smoke |

Existing `requirements.txt` / `applications/requirements.txt` / `requirements-dev.txt` were **not deleted**.

## Known packaging gaps (not G3-01 semantic defects)

- Docker API image installs unpinned `requirements.txt` + `applications/requirements.txt` and does **not** copy `database/` or `knowledge/` and does **not** install Playwright. Repo-checkout runtime is the G3-01 definition. Image completeness belongs to G3-02/G3-03.
- CI/Docker declare Python **3.12**; Gate 1/2 + this freeze were proven on **CPython 3.14.6 Windows**. Linux 3.12 must re-run the smoke (0 diffs) before production cutover.
- `BTE_LOG_LEVEL` appears in env templates but is not read by Applications API (log level is code default `INFO`).

## Test matrix

| Environment | Result |
|-------------|--------|
| Existing frozen developer Python | `pip check` OK; Gate 1/2 already proven |
| Clean Python venv + `requirements-prod.txt` | PASS |
| Clean `npm ci` + `npm run build:result` | PASS |
| Clean official PDF (Dũng) | PASS `%PDF-` 174264 bytes |
| Clean official DOCX (Dũng) | PASS; Dụng / Hỷ / Điều hậu / TIẾT present |
| Ten-case analytical probe | **0 diffs** |

Do not start G3-02 automatically.
