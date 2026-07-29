# Phase 3 Gate Review — Pattern Engine Single Source of Truth

**Date:** 2026-07-27  
**Scope:** Verification only — no code changes in this review  
**Reviewer:** AI gate review (repository search + production path trace + regression tests)

---

## Executive summary

| Gate item | Result |
|-----------|--------|
| CHECK 1 — Producer inventory | **PASS** — one canonical production producer per type |
| CHECK 2 — Production flow → Portal | **PASS** — Portal reads stored `data.pattern` JSON only |
| CHECK 3 — RuleContext ownership | **PASS (production path)** — created in Pattern Engine; downstream does not rebuild in analyze flow |
| CHECK 4 — `_merge_score_into_rule_context` | **PASS** — all writes are SAFE score enrichment |
| CHECK 5 — Layer equality | **PASS** — automated tests confirm engine ≡ AnalysisResult ≡ API |

**Gate recommendation:** **APPROVE Phase 3**

**Residual note (non-blocking):** Score/Interpretation engines still contain **fallback** `RuleContextBuilder.build()` paths for non-production callers. These are not invoked when the orchestrator passes the Pattern Engine–built context (`bazi` + `wuxing` present).

---

## CHECK 1 — Producer inventory

### `PatternResult`

| File | Function / symbol | Production? | Deprecated? |
|------|-------------------|-------------|-------------|
| `engines/pattern_engine/engine.py` | `PatternResult` (dataclass), `PatternEngine.calculate()` | **Yes** — canonical SSOT | **Canonical (Phase 3)** |
| `applications/api/services/pattern_truth.py` | `build_pattern_view(result)` | Consumer of `PatternResult` | Canonical view mapper |
| `engines/pattern/__init__.py` | Re-export `PatternResult` | Compat shim to `pattern_engine` | Legacy alias package |
| `engines/pattern/engine.py` | Re-export | Same | Legacy alias |
| `engines/bazi_engine/pattern/pattern.py` | `PatternResult` class | **No** | **LEGACY** — old bazi_engine pattern package |
| `engines/bazi_engine/pattern/calculator.py` | `build_result()` → `PatternResult` | **No** | **LEGACY** |
| `engines/bazi_engine/pattern/service.py` | Returns `PatternResult` | **No** | **LEGACY** |
| `engines/bazi_engine/models.py` | `PatternResult` (nested in Bazi models) | **No** | Different domain object — name collision |
| `engines/pattern_engine/models/pattern_result.py` | `PatternResultModel` | **No** | Internal alternate model — not wired to `PatternEngine.calculate` |
| `engines/pattern_engine/calculators/combination.py` | Returns `PatternResultModel` | **No** | **LEGACY / dormant** calculator path |

**Production producer:** `PatternEngine.calculate()` in `engines/pattern_engine/engine.py` only.

---

### `RuleContext`

| File | Function | Production? | Deprecated? |
|------|----------|-------------|-------------|
| `engines/pattern_engine/rule_context_bridge.py` | `build_rule_context()` → `RuleContextBuilder.build()` | **Yes** — invoked inside `PatternEngine.calculate()` | **Canonical (Phase 3)** |
| `engines/rule_contract/context_builder.py` | `RuleContextBuilder.build()`, `build_rule_context()` | Library — called **from Pattern Engine** in prod | Canonical builder (not a second producer in prod path) |
| `engines/score_engine/engine.py` | `_to_rule_context()` | **Fallback only** in prod | If `bazi` + `wuxing` in dict → **returns input, no rebuild** |
| `engines/interpretation_engine/engine.py` | `_to_rule_context()` | **Fallback only** in prod | Same early-return when full context passed |
| `engines/score_engine/base/generic_score_calculator.py` | `resolve_rule_context()` | **Fallback only** | `_looks_like_rule_context` → no rebuild in prod |
| `tests/rule_contract/test_context_builder.py` | Direct `RuleContextBuilder().build()` | Test only | — |
| `tests/golden_dataset/*` | Optional upstream payloads | Test/tooling | — |
| `applications/api/services/orchestrator.py` | `_merge_score_into_rule_context()` | Enriches **score slice** of pipeline copy | Not a RuleContext **creator** |

**Production creation:** `PatternEngine.calculate()` → `rule_context_bridge.build_rule_context()` only.

---

### `PatternView`

| File | Function | Production? | Deprecated? |
|------|----------|-------------|-------------|
| `applications/api/models/analysis_result.py` | `PatternView` dataclass, `to_dict()` | **Yes** — `AnalysisResult.pattern` type | Canonical contract type |
| `applications/api/services/pattern_truth.py` | `build_pattern_view()` | **Yes** — maps `PatternResult` → `PatternView` | Canonical serializer |
| `engines/pattern_engine/engine.py` | `PatternResult.to_portal_dict()` | Internal serialization helper | Used by `build_pattern_view` |
| `engines/pattern_engine/rule_context_bridge.py` | Doc reference to PatternView signals | Enriches `PatternResult` fields | Not a separate `PatternView` producer |

**Removed from production:** `OrchestratorService._shape_pattern()` — **not found** in repository (grep: 0 matches).

---

## CHECK 2 — Production flow trace

### Deployment entrypoints

| Layer | Entry |
|-------|-------|
| API | `applications.api.app:app` → `POST /api/v1/analyze` |
| Portal | `applications.customer_portal.app:app` → proxies `/backend/api/v1/*` |

### End-to-end trace

```
Browser (analyze.html)
  analyze.js → BtePortal.post("/api/v1/analyze", input)
    → fetch("/backend/api/v1/analyze")
      → Customer Portal proxy (customer_portal/app.py)
        → Applications API (routes/v1.py analyze_endpoint)
          → OrchestratorService.analyze()
            → PatternEngine.calculate(PatternContext)
              → PatternResult + rule_context
            → build_pattern_view(pattern_result) → PatternView
            → AnalysisResult.pattern = pattern_view
            → payload["pattern"] = analysis.pattern_dict()
    → BtePortal.saveLastResult({ input, data })
      → ResultStore sessionStorage `bte_last_result`

Browser (result.html)
  result.js → ResultStore.loadForView()
    → data = last.data
    → show("pattern"): payload = data.pattern
      → BtePresenters.pattern(payload)   [presenters/pattern.js renderPattern]
        → resolveValue(data, field) per FIELDS keys
        → DOM #stageView innerHTML
```

### Portal uses `AnalysisResult.pattern` only

| Portal module | Source | Computes pattern? |
|---------------|--------|-------------------|
| `result.js` | `data.pattern` from store | **No** |
| `presenters/pattern.js` | Argument = `data.pattern` JSON | **No** — display labels (`PATTERN_LABELS`) for codes only |
| `presenters/summary_builder.js` | `payload.pattern` for executive overview | **No** — reads same JSON keys |

Pattern tab does **not** re-POST analyze, does **not** call engines, does **not** scrape interpretation for pattern fields (Phase 3 removed orchestrator scrape path).

---

## CHECK 3 — RuleContext ownership

### Where RuleContext is created (production analyze path)

```
PatternEngine.calculate()
  → build_rule_context(calendar, bazi, pattern_result)
    → RuleContextBuilder.build(calendar=…, bazi=…, pattern=…)
  → result.rule_context = rule_context
```

Orchestrator then:

```python
pipeline_ctx = dict(pattern_result.rule_context or {})
score = self.score_engine.calculate(pipeline_ctx)
interpretation = self.interpretation_engine.run(pipeline_ctx)
```

### Downstream engines — rebuild behavior

| Engine | Rebuild in production? | Mechanism |
|--------|------------------------|-----------|
| **Score Engine** | **No** | `_to_rule_context`: if `"bazi" in context and "wuxing" in context` → return same dict (line 153–154) |
| **Interpretation Engine** | **No** | Same guard (line 227–228) |
| **Report Engine** | **No** | No `RuleContextBuilder` / `_to_rule_context` usage in `engines/report_engine/` |

### Fallback rebuild paths (exist but not used in prod analyze)

Score and Interpretation still contain `RuleContextBuilder().build()` fallbacks when input lacks `wuxing` + `bazi` dict keys (legacy callers, tests, direct engine invocation). **Not invoked** when orchestrator passes Pattern Engine output.

**CHECK 3 verdict:** Production analyze flow creates RuleContext **once** inside Pattern Engine; Score and Interpretation **consume** the shared dict without calling `RuleContextBuilder.build()`.

---

## CHECK 4 — `_merge_score_into_rule_context` audit

**Location:** `applications/api/services/orchestrator.py`

**Called:** After `score_engine.calculate(pipeline_ctx)`, before `interpretation_engine.run(pipeline_ctx)`.

**Target:** `pipeline_ctx` — shallow copy of `pattern_result.rule_context` (not `PatternResult` itself).

### Fields written

| Field / key | Value source | Classification |
|-------------|--------------|----------------|
| `pipeline_ctx["score"]["total_score"]` | `ScoreResult.total_score` | **SAFE** — score section enrichment |
| `pipeline_ctx["score"]["strength_score"]` | `ScoreResult.strength_score` | **SAFE** |
| `pipeline_ctx["score"]["ten_god_score"]` | `ScoreResult.ten_god_score` | **SAFE** |
| `pipeline_ctx["score"]["pattern_score"]` | `ScoreResult.pattern_score` | **SAFE** |
| `pipeline_ctx["score"]["useful_god_score"]` | `ScoreResult.useful_god_score` | **SAFE** |
| `pipeline_ctx["score"]["shensha_score"]` | `ScoreResult.shensha_score` | **SAFE** |
| `pipeline_ctx["score"]["luck_score"]` | `ScoreResult.luck_score` | **SAFE** |
| `pipeline_ctx["score"]["grade"]` | `ScoreResult.grade` | **SAFE** |
| `pipeline_ctx["score"]["confidence"]` | `ScoreResult.confidence` | **SAFE** |
| `pipeline_ctx["score"]["recommendation"]` | `ScoreResult.recommendation` | **SAFE** |
| `pipeline_ctx["score"]["success"]` | `ScoreResult.success` | **SAFE** |
| `pipeline_ctx["strength_score"]` (top-level) | `ScoreResult.strength_score` | **SAFE** — flat alias for rule matchers |

### Not modified by merge

- `pipeline_ctx["pattern"]` (dict from RuleContext — not overwritten with `PatternResult` object)
- `pipeline_ctx["bazi"]`, `wuxing`, `calendar`, `ten_gods`, `useful_god`, `strength` (pre-score stubs)
- `PatternResult` fields (`pattern`, `cach_cuc`, `than`, …)
- `pattern_result.rule_context` original reference for `score` subsection (orchestrator assigns **new** dict to `pipeline_ctx["score"]` only)

**CHECK 4 verdict:** **0 VIOLATIONS** — all writes are post-Score enrichment on orchestrator-owned pipeline context.

---

## CHECK 5 — Pattern equality chain

### Regression case: Male, 21/01/1987, 04:30

| Layer | Expected highlights |
|-------|---------------------|
| Pattern code | `chinh_quan` |
| Cách cục | `Chính Quan` |
| Thân (element) | `Kim` |
| Dụng thần | `Chính Quan` |

### Automated verification (gate review execution)

```
tests/pattern                          → 7 passed
tests/rule_contract/test_context_builder → 6 passed
applications/api/tests/test_phase3_unified_pattern.py → 5 passed
applications/api/tests/test_production_readiness.py   → 3 passed
applications/api/tests/test_phase2_unified_bazi.py    → 4 passed
```

Key tests:

| Test | Asserts |
|------|---------|
| `test_pattern_engine_produces_rule_context` | Engine emits `rule_context` with `wuxing`, `pattern.main_pattern` |
| `test_pattern_view_matches_engine` | `build_pattern_view` ≡ `to_portal_dict()`; `than=Kim`, `dung_than=Chính Quan` |
| `test_orchestrator_pattern_payload_matches_engine` | `payload["pattern"]` matches engine; no `matched_rules` / `error` in API |
| `test_api_analyze_pattern_matches_engine` | HTTP `data.pattern` matches engine |
| `test_analysis_result_pattern_slice` | `analysis.pattern_dict()` ≡ `PatternView.to_dict()` |

### Equality chain

```
PatternEngine.calculate() → PatternResult
  ≡ PatternResult.to_portal_dict()
  ≡ build_pattern_view() → PatternView.to_dict()
  ≡ AnalysisResult.pattern_dict()
  ≡ HTTP response.data.pattern
  ≡ ResultStore last.data.pattern
  ≡ renderPattern(last.data.pattern) DOM text
```

Internal fields **excluded** from API/Portal (per contract): `matched_rules`, `error`, `rule_context`.

---

## Provenance fingerprints (API)

```json
"pattern_source": {
  "engine": "engines.pattern_engine.engine.PatternEngine",
  "method": "calculate",
  "contract": "pattern_rule_context_v1",
  "view": "applications.api.services.pattern_truth.build_pattern_view"
}
```

`meta.rule_context_built_once: true` when calendar+bazi supplied to Pattern Engine.

---

## Open items (post-Phase 3, not gate blockers)

1. **Legacy pattern packages** — `engines/bazi_engine/pattern/*`, dormant `pattern_engine/calculators/*` remain in repo (not production path).
2. **Fallback RuleContext rebuild** — Score/Interpretation `_to_rule_context` fallbacks still exist for non-orchestrator callers; Phase 4+ may remove or gate behind explicit legacy API.
3. **`than_vuong_nhuoc`** — Pre-Score strength uses heuristic/month status from RuleContext (not Score `strength_score`); may refine when Score slice becomes authoritative in a later phase.
4. **Full `AnalysisResult` HTTP envelope** — `pattern` is authoritative on `data.pattern`; top-level `AnalysisResult.to_dict()` wrapper not yet exposed as single JSON root.

---

## Gate decision

| Status | **APPROVE Phase 3** |
|--------|---------------------|
| Condition | Production path must continue to pass full RuleContext from Pattern Engine to Score/Interpretation |
| Next step | Await stakeholder sign-off before Phase 4 |

---

*End of Phase 3 Gate Review.*
