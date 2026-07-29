# Phase 2 Gate Review — Unified Bazi Truth

**Date:** 2026-07-27  
**Scope:** Verification only — no code changes in this review  
**Reviewer:** AI gate review (repository search + production path trace + regression tests)

---

## Executive summary

| Gate item | Result |
|-----------|--------|
| CHECK 1 — Symbol / legacy search | **PASS** — production path uses sanctioned producers only |
| CHECK 2 — Production request trace | **PASS** — Portal renders stored `data.bazi` JSON; no re-POST on `/result` |
| CHECK 3 — Layer equality | **PASS** — Engine ≡ `AnalysisResult.bazi` ≡ API JSON (automated tests) |
| CHECK 4 — No legacy producer in production path | **PASS** |
| CHECK 5 — Single producer per pillar attribute | **PASS** (with display-only Portal metadata noted) |

**Gate recommendation:** **APPROVE Phase 2** for production Bazi single-source-of-truth.

**Residual risk (non-blocking):** Legacy stacks (`api/`, `engines/bazi_engine/pillars/*`) remain in the repository but are **not wired** to `applications.api.app:app` or the Customer Portal. Cleanup is scheduled for later phases per `docs/legacy_cleanup_plan.md` (frozen).

---

## CHECK 1 — Repository symbol search

### `calculate_bazi`

| File | Function / symbol | Used? | Deprecated? | Production? |
|------|-------------------|-------|-------------|-------------|
| `api/routers/bazi.py` | `calculate_bazi()` | Yes — legacy HTTP route `POST /` on legacy `api.app` | **LEGACY** | **No** — not `applications.api.app` |
| `api/schemas/common.py` | `calculate_bazi: bool` field | Yes — legacy request schema | **LEGACY** | **No** |
| `docs/phase0_architecture_lock.md` | documentation | — | frozen doc | — |
| `docs/legacy_cleanup_plan.md` | documentation | — | frozen doc | — |

### `build_bazi`

| File | Function / symbol | Used? | Deprecated? | Production? |
|------|-------------------|-------|-------------|-------------|
| `applications/api/services/bazi_truth.py` | `build_bazi_view()` | Yes — **authoritative enrichment** | **Canonical (Phase 2)** | **Yes** |
| `applications/api/services/orchestrator.py` | imports `build_bazi_view` | Yes | Canonical | **Yes** |
| `applications/api/tests/test_phase2_unified_bazi.py` | test assertions | Yes | test only | — |
| `engines/rule_contract/context_builder.py` | `_build_bazi()` | Yes — **serializes** existing `BaziChart` to dict for rules | Consumer, not producer | Indirect (Score path; not Portal) |
| `docs/*` | references | — | frozen docs | — |

**Note:** `build_bazi_view` is the sanctioned Phase 2 view builder. It does **not** recalculate pillars; it enriches an existing `BaziChart`.

### `make_bazi`

| Result |
|--------|
| **No matches** in repository |

### `build_chart`

| File | Function / symbol | Used? | Deprecated? | Production? |
|------|-------------------|-------|-------------|-------------|
| `engines/bazi_engine/service.py` | `BaziService.build_chart()` | Yes — wraps `BaziEngine` via engine context | Alternate service API | **No** — not imported by `applications/api` |
| `engines/bazi_engine/constants.py` | `OP_BUILD_CHART` | Yes — operation label | Internal | **No** |
| `engines/core/enums.py` | `BUILD_CHART` enum | Yes | Internal | **No** |
| `tests/bazi/test_bazi_engine.py` | `test_build_chart` | Yes | test only | — |

### `GanzhiAlgorithm`

| File | Function / symbol | Used? | Deprecated? | Production? |
|------|-------------------|-------|-------------|-------------|
| `engines/calendar_engine/algorithms/ganzhi.py` | `GanzhiAlgorithm` class | Yes — shared calendar math | **Canonical library** | Yes (library) |
| `engines/bazi_engine/engine.py` | `GanzhiAlgorithm.year`, `.day`, STEM/BRANCH | Yes — **pillar producer** | Canonical | **Yes** |
| `engines/calendar_engine/engine.py` | `GanzhiAlgorithm.year` | Yes — calendar year can/chi display | Canonical | **Yes** (calendar slice only) |
| `engines/calendar_engine/algorithms/hour_ganzhi.py` | imports `GanzhiAlgorithm` | Yes | Internal to calendar algorithms | **No** on prod Bazi path |
| `docs/bazi_data_flow_integration_audit.md` | documentation | — | frozen | — |

**Assessment:** `GanzhiAlgorithm` is a **shared read-only library**. Production Bazi pillars are produced only inside `BaziEngine.build()`. CalendarEngine uses it for calendar metadata, not for `data.bazi`.

### `PillarBuilder`

| File | Function / symbol | Used? | Deprecated? | Production? |
|------|-------------------|-------|-------------|-------------|
| `engines/bazi_engine/pillars/pillar_builder.py` | `PillarBuilder` class | Yes — standalone package | **LEGACY** | **No** |
| `engines/bazi_engine/pillars/pillar_service.py` | references `PillarBuilder` | Yes | **LEGACY** | **No** |
| `docs/*` | documentation | — | frozen | — |
| `tasks/engines/bazi.md` | task checklist | — | — | — |

**Import graph:** No file under `applications/` imports `engines.bazi_engine.pillars`.

### `legacy_bazi`

| Result |
|--------|
| **No matches** in repository |

### Hidden duplicate calculation (search: `duplicate.*calculation`, `hidden.*duplicate`)

| Result |
|--------|
| **No explicit matches** |

**Related shared primitives (not duplicate producers):**

| Primitive | Production Bazi producer | Other use |
|-----------|------------------------|-----------|
| `JulianDay.day_number` | `BaziEngine.build()` (day pillar) | `CalendarEngine.build()` (calendar JDN field) |
| `SolarTermEngine` | `BaziEngine.build()` (year boundary, month pillar) | `CalendarEngine.build()` (current solar term name) |
| `HIDDEN` stem map | `BaziEngine.build()` (flat `hidden_stems`) | `bazi_truth._slice_hidden_stems()` (per-pillar grouping only) |

Legacy duplicate implementations exist only inside `engines/bazi_engine/pillars/*` (e.g. `day_pillar.py` imports `JulianDay` independently). That package is **not** on the production path.

---

## CHECK 2 — Production request trace

### Canonical deployment

| Component | Entry |
|-----------|-------|
| API | `applications.api.app:app` (`configs/services.json`, `deployment/*`) |
| Portal | `applications.customer_portal.app:app` (proxies API) |

Legacy `api.app:app` and `main.py` default are **not** production SSOT.

### End-to-end trace

```
Browser (analyze.html)
  analyze.js: BtePortal.post("/api/v1/analyze", input)
    → fetch("/backend/api/v1/analyze")          [api.js]
      → Customer Portal proxy                   [customer_portal/app.py backend_proxy]
        → httpx → Applications API              [settings.api_base_url]
          → POST /api/v1/analyze                [applications/api/routes/v1.py analyze_endpoint]
            → OrchestratorService.analyze()     [orchestrator.py]
              → _run(stage="analyze")
                → CalendarEngine.build()
                → BaziEngine.build(calendar)
                → build_bazi_view(chart)        → BaziView
                → AnalysisResult(bazi=bazi_view)
                → payload["bazi"] = analysis.bazi_dict()
            → APIResponse { success, data: { …, bazi, … } }
      → analyze.js: res.data
        → BtePortal.saveLastResult({ input, data })  [result_store.js save()]
          → sessionStorage/localStorage key `bte_last_result`
  window.location.assign("/result")

Browser (result.html)
  result.js: BtePortal.ResultStore.loadForView()
    → last.data  (same object graph from analyze; NO re-POST)
    → show("bazi"): data.bazi passed to presenters
      → BtePresenters.bazi(payload)             [presenters/bazi.js renderBazi]
        → DOM: #stageView innerHTML
          pillar stem/branch/ten_god/truong_sinh/nap_am/hidden from JSON fields
```

### Portal reads `AnalysisResult.bazi` equivalent

The API does not yet expose a top-level `AnalysisResult` JSON envelope to the Portal. Phase 2 places authoritative Bazi at:

- In orchestrator: `AnalysisResult.bazi` (`BaziView`)
- In HTTP response: `response.data.bazi` = `analysis.bazi_dict()` = `BaziView.to_dict()`

Portal persistence stores the full `data` object:

```javascript
// analyze.js
BtePortal.saveLastResult({ input: input, data: data });
// data.bazi is the authoritative slice
```

```javascript
// result.js
var data = last.data;
view.innerHTML = map[stage](payload);  // stage "bazi" → data.bazi
```

```javascript
// presenters/bazi.js — reads fields only; no Engine calls
pillarStem(pillar)      → pillar.stem
pillarBranch(pillar)    → pillar.branch
tenGodAt(bazi, pillar)  → pillar.ten_god || bazi.ten_gods[index]
growthAt(pillar)        → pillar.truong_sinh
nayinAt(pillar)         → pillar.nap_am
hiddenAt(pillar, slice) → pillar.hidden_stems || grouped bazi.hidden_stems
```

**Portal display metadata** (`STEM_META`, `BRANCH_ELEMENT`, `BRANCH_HIDDEN_COUNT` in `bazi.js`) is used for **CSS element coloring and flat-list grouping**. It does **not** compute pillars or override API values.

---

## CHECK 3 — Layer equality

### Critical regression case

**Input:** Male, 21/01/1987, 04:30, Hà Tây / Hà Nội timezone field (calendar uses local civil time).

| Pillar | Expected |
|--------|----------|
| Year | Bính Dần |
| Month | Tân Sửu |
| Day | Canh Ngọ |
| Hour | Mậu Dần |

### Automated verification (executed at gate review)

```
pytest tests/bazi -q
  → 26 passed, 6 subtests passed

pytest applications/api/tests/test_production_readiness.py \
       applications/api/tests/test_phase2_unified_bazi.py -q
  → 7 passed
```

| Layer | Mechanism | 1987-01-21 04:30 |
|-------|-----------|------------------|
| **BaziEngine** | `test_engine_chart_matches_critical_case` | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| **AnalysisResult** | `test_bazi_view_and_chart_stay_aligned` | `BaziView.to_dict()` matches chart; `ten_gods` synced |
| **Orchestrator payload** | `test_orchestrator_payload_matches_engine` | `payload["bazi"]` pillars match engine |
| **API JSON** | `test_api_analyze_matches_engine_for_critical_case` | `data.bazi` + `calendar.*_can_chi` match |
| **Portal contract** | `test_calendar_and_bazi_are_portal_friendly` (03:30 sample) | nap_am, truong_sinh, ten_god fields present |

**Equality chain:**

```
BaziEngine.build() pillars
  == BaziView (AnalysisResult.bazi) pillar stem/branch/ten_god/nap_am/truong_sinh
  == payload["bazi"] (analysis.bazi_dict())
  == HTTP response.data.bazi
  == ResultStore last.data.bazi
  == renderBazi(last.data.bazi) DOM text
```

---

## CHECK 4 — Legacy producer audit (production path only)

### Production producers (allowed)

| Step | Module | Role |
|------|--------|------|
| 1 | `CalendarEngine.build` | Solar/lunar/JDN/term inputs (not `data.bazi`) |
| 2 | `BaziEngine.build` | Four pillars, flat `hidden_stems`, base `ten_gods` |
| 3 | `build_bazi_view` | Enrichment → `BaziView` (nap_am, truong_sinh, per-pillar hidden, ten_god labels) |
| 4 | `AnalysisResult` | Holds authoritative `bazi` slice |
| 5 | `analysis.bazi_dict()` | Serializes to `data.bazi` |

### Not in production path (legacy / alternate stacks)

| Module | Why excluded |
|--------|--------------|
| `api/routers/bazi.py` → `PipelineService` | Legacy `api.app` stack |
| `engines/bazi_engine/pillars/pillar_builder.py` | Not imported by `applications/api` |
| `engines/bazi_engine/pillars/pillar_service.py` | Not imported by `applications/api` |
| `engines/bazi_engine/service.py` `BaziService.build_chart` | Not imported by `applications/api` |
| `engines/integration/orchestrator.py` | Alternate integration wiring |
| `engines/calendar_engine/algorithms/hour_ganzhi.py` | Not used by `BaziEngine` (engine uses `_hour_pillar`) |

### Removed from production path (Phase 2)

| Former duplicate | Status |
|------------------|--------|
| `OrchestratorService._shape_bazi()` | **Removed** |
| `OrchestratorService._ten_god()` | **Removed** |
| Orchestrator nap_am / truong_sinh CSV loaders | **Moved** to `bazi_truth.py` |
| Stub `ten_gods = ["Tỷ Kiên"]×4` | **Removed** from `BaziEngine.build()` |

**CHECK 4 verdict:** No legacy Bazi **producer** remains inside `applications/api` → Portal production path.

---

## CHECK 5 — Single producer per pillar attribute

| Attribute | Producer | Enrichment | Portal read path | Recalculated in Portal? |
|-----------|----------|------------|------------------|-------------------------|
| **Year stem/branch** | `BaziEngine.build()` (`GanzhiAlgorithm.year` + Lập Xuân via `SolarTermEngine`) | `build_bazi_view` copies pillars | `bazi.year_pillar.stem/branch` | No |
| **Month stem/branch** | `BaziEngine.build()` (`SolarTermEngine.get_bazi_month` + Ngũ Hổ Độn) | same | `bazi.month_pillar.*` | No |
| **Day stem/branch** | `BaziEngine.build()` (`JulianDay` + `GanzhiAlgorithm.day`) | same | `bazi.day_pillar.*` | No |
| **Hour stem/branch** | `BaziEngine.build()` (`_hour_pillar` Ngũ Thử Độn) | same | `bazi.hour_pillar.*` | No |
| **Hidden stem (flat)** | `BaziEngine.build()` (`HIDDEN` map) | copied to `BaziView.hidden_stems` | `bazi.hidden_stems` | No (grouping only) |
| **Hidden stem (per pillar)** | sliced from flat list in `bazi_truth._slice_hidden_stems` | `PillarView.hidden_stems` | `pillar.hidden_stems` or slice of flat | No |
| **Ten God** | `ten_god_name()` in `BaziEngine.build()` | reaffirmed in `bazi_truth._pillar_view` (same logic) | `pillar.ten_god` / `bazi.ten_gods[i]` | No |
| **Trường Sinh** | — | `bazi_truth` CSV `truong_sinh_nhat_chu.csv` | `pillar.truong_sinh` | No |
| **Nạp Âm** | — | `bazi_truth` CSV `luc_thap_hoa_giap/du_lieu.csv` | `pillar.nap_am` | No |
| **Day master element / Âm Dương** | — | `bazi_truth` via `ten_god.py` helpers | `bazi.day_master*` + Portal `stemMeta` for display | Display metadata only |

**Downstream engines** (Pattern / Score / Interpretation) receive `bazi_chart` after `sync_chart_from_view()`, so `ten_gods` / `shensha` match `AnalysisResult.bazi`.

---

## Provenance fingerprint

Production responses include:

```json
"bazi_source": {
  "engine": "engines.bazi_engine.engine.BaziEngine",
  "method": "build",
  "contract": "li_chun_jdn_v1",
  "view": "applications.api.services.bazi_truth.build_bazi_view"
}
```

---

## Open items (post-Phase 2, not gate blockers)

1. **Legacy stack removal** — `api/routers/bazi.py`, `engines/bazi_engine/pillars/*` (per `legacy_cleanup_plan.md`).
2. **Full `AnalysisResult` HTTP envelope** — other stages still on orchestrator `payload` dict; only `bazi` slice is authoritative today.
3. **Portal `day_master_element` / `day_master_yin_yang`** — API provides these on `data.bazi`; Bazi tab summary uses `stemMeta` lookup for element/yin-yang display (cosmetic; stem text comes from API).

---

## Gate decision

| Status | **APPROVE Phase 2** |
|--------|---------------------|
| Condition | Legacy code may remain in repo but must not be wired to production entrypoints without explicit phase approval |
| Next step | Await stakeholder sign-off before Phase 3 (Pattern / Score / RuleContext unification) |

---

*End of Phase 2 Gate Review.*
