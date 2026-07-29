# API Score Trace Report

| Item | Value |
|------|-------|
| Document | `API_SCORE_TRACE_REPORT.md` |
| Project | BTE Platform V1.0 |
| Sprint | Sprint 2A.1 — API Contract Verification |
| Source | `docs/reports/PIPELINE_DATA_TRACE_REPORT.md` |
| Scope | Runtime **score** data contract (backend ↔ frontend) only |
| Case | Male · 21/01/1987 · 04:30 · Asia/Ho_Chi_Minh |
| Date | 2026-07-28 |
| Constraints | Report only — **no fixes**, no scoring / Rule DB / Knowledge changes |

---

## Executive Summary

Backend → JSON for all eight score scalars is **intact** on the production analyze path after Sprint 2A (`ScoreResult.to_portal_dict` → `ScoreView` → `data.score`).

The main contract gaps are **frontend binding**, not serialization loss:

| Field | Backend → JSON | Frontend state | Đánh Giá render |
|-------|----------------|----------------|-----------------|
| `total_score` | OK (`55.25`) | OK | OK (summary card) |
| `strength_score` | OK (`45`) | OK | OK (card + gauge) |
| `pattern_score` | OK (`100`) | OK | OK (summary card) |
| `ten_god_score` | OK (`100`) | OK | OK (extras; series preferred) |
| `wuxing_score` | OK (`0`) | OK | **PARTIAL** — series of **counts** shown; scalar 0 not a top card |
| `useful_god_score` | OK (`20`) | OK | **NOT RENDERED** |
| `shensha_score` | OK (`100`) | OK | **NOT RENDERED** |
| `luck_score` | OK (`0`) | OK | **NOT RENDERED** |

Canonical overall field name is **`total_score`**. Frontend accepts `overall_score` as an alias only; API never emits `overall_score`.

OpenAPI has **no typed Score schema** (`APIResponse.data: dict[str, Any]`). Portal has **no TypeScript score types**.

---

## End-to-end pipeline (score slice)

```text
Calculator (GenericScoreCalculator / FinalScoreCalculator)
    ↓
ScoreResult  (engines/score_engine/result.py)
    ↓
ScoreEngine.calculate / append_score_to_rule_context
    ↓  (Interpretation reads composed RuleContext.score for matching —
        InterpretationResult / InterpretationView do NOT re-export score fields)
ScoreView via build_score_view  (applications/api/services/score_truth.py)
    ↓
AnalysisResult.score_dict() → payload["score"]
    ↓
APIResponse { data: { score: {...}, ... } }  (routes/v1.py analyze)
    ↓
JSON Response
    ↓
BtePortal.post("/api/v1/analyze")  (customer_portal/static/js/api.js)
    ↓
analyze.js → ResultStore.save({ input, data })  (result_store.js)
    ↓
result.js show("score") → data.score
    ↓
BtePresenters.score(score)  (presenters/score.js)
```

**InterpretationResult:** score dimensions are **inputs to matching** via composed RuleContext (`score.total_score`, `strength_score`, …). They are **not** mapped onto `data.interpretation`. UI score tab reads **`data.score` only**.

---

## 1. Complete score field mapping

Case values below are live `OrchestratorService.analyze(...)` for 21/01/1987.

### Shared name check

| Layer | Overall field name |
|-------|--------------------|
| `ScoreResult` | `total_score` |
| `ScoreView` / JSON | `total_score` |
| OpenAPI | untyped `data` — no property |
| Frontend `score.js` SUMMARY | prefers `total_score`, aliases `overall_score` / `overall` / `final_score` / `score` |
| Frontend `executive.js` | `h.total_score` (from summary_builder pick including `overall_score` alias) |

**Verdict:** Frontend expects **`total_score` primarily**; **`overall_score` is fallback alias only**. Backend does **not** emit `overall_score`.

---

### `total_score`

| Stage | Location | Property / behavior | Value (case) |
|-------|----------|---------------------|--------------|
| Calculator | `FinalScoreCalculator.calculate` | `result.score` (weighted sum) | 55.25 |
| ScoreResult | `engines/score_engine/engine.py` | `result.total_score` | 55.25 |
| Pipeline | orchestrator Stage 6 | `analysis.score` via `build_score_view` | 55.25 |
| InterpretationResult | — | not exported on interpretation view | N/A |
| API DTO | `ScoreView.total_score` → `to_dict()` | `total_score` | 55.25 |
| JSON | `data.score.total_score` | | 55.25 |
| API client | `api.js` parse JSON | no rename | 55.25 |
| State | `result_store.js` `data.score` | opaque | 55.25 |
| Render | `score.js` SUMMARY id=`overall` | `pick(..., ["total_score", "overall_score", …])` | **55.25** |

**Differs?** No numeric loss.

---

### `strength_score`

| Stage | Location | Property | Value |
|-------|----------|----------|-------|
| Calculator | `StrengthScoreCalculator` | `weighted_score` → module `strength` | 45.0 |
| ScoreResult | `result.strength_score` | | 45.0 |
| API / JSON | `data.score.strength_score` | | 45.0 |
| State | `data.score.strength_score` | | 45.0 |
| Render | SUMMARY `than` keys + `findStrengthValue` gauge | | **45** |

**Differs?** No.

---

### `wuxing_score`

| Stage | Location | Property | Value |
|-------|----------|----------|-------|
| Calculator | `WuxingScoreCalculator` | module `wuxing` (clamped) | 0.0 |
| ScoreResult / JSON | `wuxing_score` | | 0.0 |
| Also emitted | `wuxing_series` | element **counts** (Mộc:4, …) | counts ≠ score |
| State | both keys present | | OK |
| Render | `findWuxingSeries` prefers `wuxing_series`; only falls back to scalar `wuxing_score` if series absent | | Bars show **counts** (4,5,6…), **not** scalar `0` |

**Differs?** Scalar `0` is in JSON/state but **not shown as “Điểm ngũ hành”**; extras show count series. Semantic mismatch at:

- `applications/customer_portal/static/js/presenters/score.js` → `findWuxingSeries` / `renderScore`

---

### `pattern_score`

| Stage | Location | Value |
|-------|----------|-------|
| Calculator | `PatternScoreCalculator` | 100.0 (clamped) |
| JSON / state | `pattern_score` | 100.0 |
| Render | SUMMARY `pattern` keys | **100** |

**Differs?** No.

---

### `ten_god_score`

| Stage | Location | Value |
|-------|----------|-------|
| Calculator | `TenGodScoreCalculator` | 100.0 |
| JSON / state | `ten_god_score` + `ten_god_series` | 100 + series |
| Render | `findTenGodSeries` prefers series; else scalar | series bars (not necessarily “100” as one card) |

**Differs?** Scalar present; UI prefers series counts/labels. No key rename loss.

---

### `useful_god_score`

| Stage | Location | Value |
|-------|----------|-------|
| Calculator | `UsefulGodScoreCalculator` | 20.0 |
| ScoreResult | `useful_god_score` | 20.0 |
| `to_portal_dict` | always emitted (incl. 0) | 20.0 |
| `ScoreView` / JSON | `useful_god_score` | 20.0 |
| State | present | 20.0 |
| Render | **no** SUMMARY key; **no** extras reader | **not displayed** |

**Loss point:** `presenters/score.js` `SUMMARY` / `renderScore` — property never read.

---

### `shensha_score`

| Stage | Location | Value |
|-------|----------|-------|
| Calculator | `ShenshaScoreCalculator` | 100.0 |
| JSON / state | `shensha_score` | 100.0 |
| Render | not bound | **not displayed** |

**Loss point:** same — `presenters/score.js`.

---

### `luck_score`

| Stage | Location | Value |
|-------|----------|-------|
| Calculator | `LuckScoreCalculator` | 0.0 (0 matched rules) |
| JSON / state | `luck_score` | 0.0 |
| Render | not bound | **not displayed** |

**Loss point:** same — `presenters/score.js`.  
(Backend 0 is an upstream/calculation fact from prior audits; this report only notes UI never shows the key.)

---

## 2. Missing mappings

| Missing | Where |
|---------|--------|
| Typed OpenAPI / Pydantic `ScoreResponse` fields | `applications/api/schemas/common.py` — `APIResponse.data: dict[str, Any]` |
| Frontend TypeScript / JSDoc score contract | Portal is plain JS; no `*.d.ts` / typed client |
| UI binding for `useful_god_score` | `presenters/score.js` |
| UI binding for `shensha_score` | `presenters/score.js` |
| UI binding for `luck_score` | `presenters/score.js` |
| Dedicated “Điểm ngũ hành” scalar card for `wuxing_score` | SUMMARY has no `wuxing_score` entry |
| `overall_score` on API | Never produced (alias only on FE) |
| Score fields on `InterpretationView` | By design — not part of interpretation portal DTO |
| `interpretation_score` production | Always `null` / omitted; SUMMARY card shows `--` |

---

## 3. Incorrect property names

| Issue | Detail |
|-------|--------|
| `overall_score` vs `total_score` | **Not incorrect on backend.** Canonical = `total_score`. FE alias list includes `overall_score` for tolerance only. |
| No rename loss on wire | Calculator → ScoreResult → ScoreView → JSON use the same snake_case names for all eight fields. |
| Possible FE confusion | SUMMARY key `pattern` also lists bare `"pattern"` as alias — safe while `data.score.pattern` is absent; would collide if a nested object appeared. |

---

## 4. Serialization issues

| Issue | File / function | Effect |
|-------|-----------------|--------|
| Historically zeros omitted for luck/useful/shensha | Fixed in Sprint 2A: `ScoreResult.to_portal_dict` always includes them | Current JSON includes `luck_score: 0` |
| `ScoreView.to_dict` still gates on `is not None` | `analysis_result.py` `ScoreView.to_dict` | OK today because `build_score_view` sets floats from portal; risk if a field left `None` |
| `details` / module internals stripped | `to_portal_dict` (intentional) | FE cannot read `details.final_score`; `findPriority` usually `--` |
| Untyped OpenAPI | `APIResponse` | Contract not enforceable in `/docs` |
| Envelope | `{ success, message, data, request_id }` | `analyze.js` correctly uses `res.data` |

No numeric mutation observed between ScoreResult and JSON for the eight fields.

---

## 5. Frontend binding issues

| Issue | Exact location | Behavior |
|-------|----------------|----------|
| Three scores never rendered | `applications/customer_portal/static/js/presenters/score.js` — `SUMMARY` (lines ~12–41) and `renderScore` | `useful_god_score`, `shensha_score`, `luck_score` ignored |
| Wuxing scalar vs series | `findWuxingSeries` in same file | When `wuxing_series` exists, UI shows **counts**, hiding scalar `wuxing_score` |
| Interpretation score card empty | SUMMARY id=`interpretation` | Expects `interpretation_score` — backend leaves null → `--` |
| State layer OK | `result_store.js` `normalizeResult` | Keeps full `data.score` object; no field filter |
| Client OK | `api.js` `api()` | No score reshape |
| Tab wiring OK | `result.js` `show("score")` | Passes `data.score` to presenter unchanged |
| Executive highlight | `summary_builder.js` `buildHighlight` + `executive.js` | Only surfaces overall via `total_score` (+ aliases), not dimension scores |

---

## 6. Exact files requiring modification

Report only — **do not implement** in this sprint task.

| Priority | File | Why |
|----------|------|-----|
| High | `applications/customer_portal/static/js/presenters/score.js` | Bind `useful_god_score`, `shensha_score`, `luck_score`; decide how to show scalar `wuxing_score` vs `wuxing_series` |
| Medium | `applications/customer_portal/static/js/i18n.js` (and locale strings) | Labels for new score cards if added |
| Medium | `applications/api/schemas/common.py` (or new `schemas/score.py`) | Typed Score DTO for OpenAPI / response_model |
| Low | `applications/api/models/analysis_result.py` `ScoreView.to_dict` | Always emit optional floats (incl. 0) symmetrically with `to_portal_dict` |
| Low | `applications/customer_portal/static/js/presenters/summary_builder.js` / `executive.js` | Only if executive dashboard should show dimension scores |
| Optional | Portal JSDoc / future TS types for `data.score` | Document canonical `total_score` and aliases |
| Do **not** touch for this contract gap | Score calculators, Rule DB, Knowledge layer | Out of scope; values already reach JSON |

---

## Consistency matrix

| Field | Backend model | API DTO (`ScoreView`) | OpenAPI | FE types | FE component bind |
|-------|---------------|------------------------|---------|----------|-------------------|
| `total_score` | Yes | Yes | No (loose) | No TS | Yes (`total_score` + aliases) |
| `strength_score` | Yes | Yes | No | No | Yes |
| `wuxing_score` | Yes | Yes | No | No | Partial (series preferred) |
| `pattern_score` | Yes | Yes | No | No | Yes |
| `ten_god_score` | Yes | Yes | No | No | Partial (series preferred) |
| `useful_god_score` | Yes | Yes | No | No | **No** |
| `shensha_score` | Yes | Yes | No | No | **No** |
| `luck_score` | Yes | Yes | No | No | **No** |
| `overall_score` | **No** | **No** | No | alias only | alias only |

---

## Special verification — `overall_score` vs `total_score`

| Question | Answer |
|----------|--------|
| Does frontend require `overall_score`? | **No.** Primary key is `total_score`. |
| Does API send `overall_score`? | **No.** |
| Will overall card break if only `total_score` exists? | **No** — `pick` finds `total_score` first. |
| Recommendation for future fixes | Keep API canonical name **`total_score`**; keep FE alias for compatibility; do not rename Public API. |

---

## Case evidence snapshot (`data.score`)

```json
{
  "total_score": 55.25,
  "strength_score": 45.0,
  "wuxing_score": 0.0,
  "pattern_score": 100.0,
  "ten_god_score": 100.0,
  "useful_god_score": 20.0,
  "shensha_score": 100.0,
  "luck_score": 0.0,
  "interpretation_score": null,
  "grade": "D+",
  "confidence": "medium"
}
```

`overall_score` absent. `wuxing_series` / `ten_god_series` present (count-like series).

---

## Conclusion

1. **Backend → JSON contract for the eight score fields is complete** for this case.  
2. **Loss is at frontend render binding**, not at ScoreResult → DTO → JSON.  
3. Canonical overall name: **`total_score`**.  
4. Files to change later: primarily **`presenters/score.js`**, optionally OpenAPI Score schema — without touching scoring algorithms, Rule Database, or Knowledge.

---

END
