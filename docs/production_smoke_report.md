# BTE Platform V1.0 — Production Smoke Report

**Run date:** 2026-07-27  
**Harness:** `validation/production_smoke_runner.py`  
**Raw JSON:** `validation/production_smoke_raw.json`  
**Architecture:** V1.0 FROZEN

---

## Executive summary

| Metric | Result |
|--------|--------|
| Total cases | 105 |
| PASS | 105 |
| FAIL | 0 |
| Pass rate | 100% |
| API + Portal pytest | 76 / 76 PASS |

**Verdict:** Production smoke **GREEN** — full pipeline completes for all validation cases including Li Chun, leap year, Zi hour, midnight, missing gender, and invalid inputs (422).

---

## Pipeline verification

Every successful case confirms:

```
Calendar → Bazi → Pattern → Score → Interpretation → Report → Narrative
```

| Stage | Validation |
|-------|------------|
| Calendar | `data.calendar` with `solar_date`, `lunar` |
| Bazi | Four pillars + `day_master` |
| Pattern | `success`, `pattern`, `cach_cuc` |
| Score | `total_score`, `success`; no internal leak |
| Interpretation | `sections[]` populated; commercial wire only |
| Report | `title`, `markdown`, `html`, `section_count` |
| Narrative | Portal shape; markdown non-empty |
| Portal contract | No `templates_used`, `details`, `matched_rule_count` on wire |

---

## Performance

| Metric | Value |
|--------|-------|
| Min latency | 10.4 ms |
| Max latency | 1967.4 ms |
| Average latency | 252.6 ms |
| Cases > 500 ms | 2 (cold start) |

**Slowest case:** `ref_1987_0121` — 1967.4 ms (first request / cold import).  
**Warm requests:** typically 150–450 ms.

See BUG-PROD-003 in `production_bug_tracker.md`.

---

## Category results

| Category | Count | PASS | FAIL |
|----------|-------|------|------|
| critical_reference | 3 | 3 | 0 |
| before_li_chun | 5 | 5 | 0 |
| after_li_chun | 5 | 5 | 0 |
| on_li_chun | 5 | 5 | 0 |
| leap_year | 5 | 5 | 0 |
| leap_month | 2 | 2 | 0 |
| solar_term | 4 | 4 | 0 |
| zi_hour | 4 | 4 | 0 |
| midnight | 2 | 2 | 0 |
| hour_boundary | 2 | 2 | 0 |
| missing_gender | 1 | 1 | 0 |
| gender_female | 1 | 1 | 0 |
| rc1_real_case | 20 | 20 | 0 |
| bazi_regression | 5 | 5 | 0 |
| hour_sweep | 12 | 12 | 0 |
| decade_grid | 13 | 13 | 0 |
| extra_boundary | 12 | 12 | 0 |
| invalid_input | 4 | 4 | 0 |

---

## API endpoint sweep

All production endpoints returned expected status on sample birth payload:

| Endpoint | Status | Notes |
|----------|--------|-------|
| `GET /api/v1/health` | 200 | OK |
| `POST /api/v1/calendar` | 200 | Pipeline stops at calendar |
| `POST /api/v1/bazi` | 200 | Through bazi |
| `POST /api/v1/pattern` | 200 | Through pattern |
| `POST /api/v1/score` | 200 | Through score |
| `POST /api/v1/interpretation` | 200 | Through interpretation |
| `POST /api/v1/report` | 200 | Through report (no narrative) |
| `POST /api/v1/narrative` | 200 | Full pipeline |
| `POST /api/v1/analyze` | 200 | Primary Portal endpoint |

---

## Portal route sweep

| Route | Status | Template |
|-------|--------|----------|
| `/dashboard` | 200 | Home |
| `/analyze` | 200 | Input form |
| `/result` | 200 | Result tabs |
| `/reports` | 200 | Report history |
| `/history` | 200 | History |
| `/profile` | 200 | Profile |
| `/login` | 200 | Login |

**UI validation (static):**

| Page | Input | Result | Calendar | Bazi | Pattern | Score | Interpretation | Narrative | Report |
|------|-------|--------|----------|------|---------|-------|----------------|-----------|--------|
| Analyze | Form + POST analyze | — | — | — | — | — | — | — | — |
| Result | — | Tab shell | Tab | Tab | Tab | Tab | Tab | Tab | via reports |
| Reports | — | — | — | — | — | — | — | Stored | Stored |

**Loading state:** `analyze.js` disables button + step messages during POST.  
**Error state:** Form validation + API error flash; `result.js` shows message if ResultStore empty.  
**Responsive:** Layout in `_layout.html` + CSS (manual visual check recommended).

**Result page:** Does not re-POST `/analyze` — reads `ResultStore` only (`result.js` L47–48).

---

## Production request trace (single case)

**Case:** `ref_1987_0121` — Browser analyze flow

### Browser

1. User fills `analyze.html` form (full_name, birth_place, datetime, gender).
2. `analyze.js` POST `/api/v1/analyze` with birth JSON.
3. Response `data` saved to `sessionStorage` via `BtePortal.saveLastResult`.
4. Navigate to `/result`.

### HTTP → API

5. `analyze_endpoint` → `orchestrator.analyze()`.
6. `attach_presentation_metadata` adds `customer` block (no engine calls).

### Orchestrator → objects

| Step | Object created | Stored |
|------|----------------|--------|
| 1 | `CalendarResult` | `payload["calendar"]` |
| 2 | `BaziChart` → `BaziView` | `analysis.bazi` |
| 3 | Feng Shui dict (optional) | `payload["feng_shui"]` |
| 4 | `PatternResult` → `PatternView` + `rule_context` | `analysis.pattern`, `rule_context` |
| 5 | `ScoreResult` → `ScoreView` | `analysis.score` |
| 6 | `InterpretationResult` → `InterpretationView` | `analysis.interpretation` |
| 7 | `ReportResult` → `ReportView` + `NarrativeView` | `analysis.report`, `analysis.narrative` |
| 8 | `AnalysisResult` aggregate | Serialized to API `data` |

### API JSON → Portal

7. `result.js` loads stored payload.
8. Tab `calendar` → `presenters/calendar.js`.
9. Tab `bazi` → `presenters/bazi.js`.
10. Tab `pattern` → `presenters/pattern.js`.
11. Tab `score` → `presenters/score.js`.
12. Tab `interpretation` → `presenters/interpretation.js`.
13. Tab `narrative` → `presenters/narrative.js` (markdown/html render).
14. `summary_builder.js` / `executive.js` aggregate for executive summary (display only).

**No engine objects exist in the browser.**

---

## Regression suite (broader)

| Suite | Command | Result |
|-------|---------|--------|
| API + Portal | `pytest applications/api/tests applications/customer_portal/tests -q` | 76 passed |
| Report module | `pytest tests/report -q` | 47 passed |
| Production-clean | `pytest --ignore=tests/golden_dataset --ignore=legacy root tests` | 380 passed |
| Full repo | `pytest --ignore=tests/golden_dataset` | 392 passed, 5 failed (legacy) |
| Golden dataset | `pytest tests/golden_dataset` | Collection error (`jsonschema`) |
| Skipped | `test_result_store` | 1 conditional (Node harness) |

---

## Failures (none in smoke)

No FAIL rows in `production_smoke_raw.json`.

---

## How to re-run

```powershell
cd BTE-Platform
py -3.13 validation/production_smoke_runner.py
```

```powershell
py -3.13 -m pytest applications/api/tests applications/customer_portal/tests -q
```

---

## Sign-off

| Check | Status |
|-------|--------|
| 100+ real-world charts | 105 cases |
| Full pipeline per case | PASS |
| Portal wire contract | PASS |
| API endpoints | PASS |
| Critical reference 1987-01-21 | PASS |
| Invalid input handling | PASS (422) |

**Production smoke status:** **STABLE** for V1.0 frozen architecture.
