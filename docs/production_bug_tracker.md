# BTE Platform V1.0 — Production Bug Tracker

**Status:** Architecture FROZEN — stabilization only  
**Last updated:** 2026-07-27  
**Smoke suite:** `validation/production_smoke_runner.py` (105 cases, 105 PASS)

---

## Summary

| Severity | Open | Queued | Fixed (stabilization) |
|----------|------|--------|------------------------|
| Critical | 0 | 0 | 0 |
| High | 0 | 0 | 0 |
| Medium | 3 | 0 | 0 |
| Low | 6 | 0 | 0 |
| Info | 1 | 0 | 0 |

**Production smoke:** 105 / 105 PASS on `/api/v1/analyze` full pipeline.  
**API + Portal pytest:** 76 / 76 PASS.

No Critical or High bugs found on the production path during stabilization. Medium/Low issues are queued — no architectural fixes applied.

---

## Bug register

### BUG-PROD-001 — Timezone parameter ignored

| Field | Value |
|-------|-------|
| **Severity** | Medium |
| **Module** | `applications/api/services/orchestrator.py` |
| **Status** | Queued |
| **Affected layers** | API input contract, Calendar (indirect) |

**Repro steps**

1. POST `/api/v1/analyze` with `timezone: "Asia/Singapore"` vs `Asia/Ho_Chi_Minh`.
2. Compare `calendar` / `bazi` output for same local datetime.

**Observed**  
`timezone` is accepted on `BirthRequest` but discarded in orchestrator (`del timezone  # reserved for future calendar localization`).

**Root cause**  
Calendar localization not implemented; parameter is a no-op.

**Risk**  
Users outside Vietnam timezone may get incorrect solar/lunar alignment if they expect timezone conversion.

**Recommended fix** (post-stabilization, non-breaking)  
Apply timezone in CalendarEngine input only; do not change `AnalysisResult` schema. Add regression cases per timezone.

---

### BUG-PROD-002 — Golden dataset suite cannot collect

| Field | Value |
|-------|-------|
| **Severity** | Medium |
| **Module** | `tests/golden_dataset/test_golden_dataset.py` |
| **Status** | Queued |
| **Affected layers** | QA tooling only (not production runtime) |

**Repro steps**

```bash
py -3.13 -m pytest tests/golden_dataset/test_golden_dataset.py --collect-only
```

**Observed**  
`ModuleNotFoundError: No module named 'jsonschema'`

**Root cause**  
Optional QA dependency not installed in validation environment.

**Risk**  
Golden dataset regression cannot run in CI/local without extra install.

**Recommended fix**  
Add `jsonschema` to dev/QA requirements or document optional install; do not change Golden Dataset files.

---

### BUG-PROD-003 — Analyze cold-start latency spike

| Field | Value |
|-------|-------|
| **Severity** | Medium |
| **Module** | Full pipeline (first request after process start) |
| **Status** | Queued |
| **Affected layers** | API perceived performance, Portal loading UX |

**Repro steps**

1. Fresh Python process.
2. First POST `/api/v1/analyze` (case `ref_1987_0121`).

**Observed**  
~1967 ms first request; subsequent requests ~150–450 ms (smoke avg 252.6 ms).

**Root cause**  
Cold import / loader initialization (score rules, interpretation DB, templates).

**Risk**  
First Portal analyze after server restart feels slow; not a correctness issue.

**Recommended fix**  
Warm-up endpoint or lazy-loader caching audit (no pipeline change).

---

### BUG-PROD-004 — `/narrative` route docstring misleading

| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Module** | `applications/api/routes/v1.py` L117 |
| **Status** | Queued |
| **Affected layers** | Documentation / developer experience |

**Repro steps**  
Read `narrative_endpoint` docstring: "Run full pipeline through NarrativeEngine."

**Observed**  
Production path uses `ReportEngine.render_from_analysis(include_narrative=True)`; `NarrativeEngine` is not called.

**Root cause**  
Docstring stale after Phase 6.

**Risk**  
Developer confusion only.

**Recommended fix**  
Update docstring only (no behavior change).

---

### BUG-PROD-005 — Narrative content identical to report

| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Module** | `engines/report_engine/portal_view.py` |
| **Status** | Known / by design (Phase 6) |
| **Affected layers** | API `data.narrative`, Portal narrative tab |

**Repro steps**

1. POST `/api/v1/analyze`.
2. Compare `data.report` and `data.narrative` fields.

**Observed**  
`title`, `markdown`, `html`, `section_count` match; no `tone` or `metrics`.

**Root cause**  
`build_narrative_portal_dict()` delegates to `build_report_portal_dict()`. WP7 `NarrativeEngine` not on production path.

**Risk**  
Narrative tab does not show polished prose distinct from report; Portal still renders correctly.

**Recommended fix**  
Future phase inside Report Engine only (architecture frozen); wire narrative polish without orchestrator duplication.

---

### BUG-PROD-006 — Legacy root tests fail

| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Module** | `tests/test_builder.py`, `tests/test_pipeline.py`, `tests/test_sentence_generator.py`, `tests/integration/test_pipeline.py` |
| **Status** | Queued (Legacy Cleanup V1) |
| **Affected layers** | CI signal only |

**Repro steps**

```bash
py -3.13 -m pytest tests/test_builder.py tests/test_pipeline.py tests/test_sentence_generator.py tests/integration/test_pipeline.py -q
```

**Observed**  
5 failures — obsolete import paths (`interpretation_engine.*`), Score-before-Pattern order.

**Root cause**  
Pre-Phase-2 test modules not updated; not on production path.

**Risk**  
Full `pytest` without exclusions shows red; production path is green.

**Recommended fix**  
Legacy Cleanup V1 — remove or relocate tests; do not change production code.

---

### BUG-PROD-007 — Score presenter legacy `details.*` fallback

| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Module** | `applications/customer_portal/static/js/presenters/score.js` |
| **Status** | Queued |
| **Affected layers** | Portal Score tab (edge cases) |

**Repro steps**  
Inspect `findWuxingSeries` / `findTenGodSeries` — reads `data.details.wuxing` when direct series missing.

**Observed**  
Production API omits `details` (by design). Fallback is dead code on happy path but could mask API regressions if partial payloads appear.

**Root cause**  
Backward compatibility for old API shape.

**Risk**  
Low — production API provides `wuxing_series` / `ten_god_series` when available.

**Recommended fix**  
Portal-only cleanup in stabilization+1; verify no old clients need `details`.

---

### BUG-PROD-008 — Portal Bazi hidden-stem display fallback

| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Module** | `presenters/bazi.js`, `presenters/summary_builder.js` |
| **Status** | Queued |
| **Affected layers** | Portal Bazi / summary display |

**Repro steps**  
If API `hidden_stems` per pillar empty, Portal uses `BRANCH_HIDDEN_COUNT` local table.

**Observed**  
Display-only fallback; does not recalculate Bazi.

**Root cause**  
Defensive UI for incomplete payloads.

**Risk**  
Could show wrong hidden stem count if API data incomplete (smoke tests show API provides data).

**Recommended fix**  
Remove fallback once API contract guaranteed; Portal-only.

---

### BUG-PROD-009 — Calendar not on AnalysisResult

| Field | Value |
|-------|-------|
| **Severity** | Info |
| **Module** | `applications/api/models/analysis_result.py`, orchestrator |
| **Status** | Known architecture note |
| **Affected layers** | Contract documentation |

**Observed**  
`calendar` lives in API `payload["calendar"]` only; no `analysis.calendar` slice or `calendar_truth`.

**Risk**  
None for Portal — reads `data.calendar` from API JSON.

**Recommended fix**  
Optional future `CalendarView` slice (requires architecture approval post-V1 freeze).

---

## Fix policy (Architecture Freeze)

| Severity | Action |
|----------|--------|
| Critical | Fix immediately (production broken) |
| High | Fix immediately (wrong data / security / blocking UX) |
| Medium | Queue — fix in stabilization window with minimal diff |
| Low / Info | Queue for Legacy Cleanup or Portal-only polish |

**Stabilization session:** No Critical/High bugs identified → **no production code fixes applied.**

---

## Changelog

| Date | Action |
|------|--------|
| 2026-07-27 | Initial tracker from smoke suite (105 PASS) + API/Portal audit |
