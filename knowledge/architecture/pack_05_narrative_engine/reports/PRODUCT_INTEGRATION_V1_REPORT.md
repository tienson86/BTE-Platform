# Product Integration V1 — Integration Report

Version: 1.0  
Status: COMPLETE (with documented gaps)  
Date: 2026-08-08  
Epic: Replace remaining legacy interpretation paths with Pack 05 `NarrativeResult`

---

## 1. Objective

Make **Portal the official consumer** of Pack 05 `NarrativeResult` for commercial prose on the Result Page, without implementing Report Engine, without modifying Foundation, and without changing Narrative Engine internals in this epic (consume public API only).

---

## 2. Contract

| Field | Role |
|-------|------|
| `data.narrative_result` | **Official** Pack 05 commercial `NarrativeResult` (`contract: pack05_narrative_result_v1`) |
| `data.narrative_result_source` | Provenance fingerprint |
| `data.interpretation` | Legacy Interpretation Engine sections — **fallback only** when Pack 05 absent |
| `data.narrative` | ReportEngine delivery (title / markdown / html) — **unchanged**; not Pack 05 |

---

## 3. Pipeline wiring (API)

After Interpretation stage, Orchestrator publishes:

1. `payload["narrative_result"]` via `build_narrative_result_dict`  
   (`applications/api/services/narrative_result_truth.py`)
2. Calls public `NarrativeEngine.compose_narrative_result(...)` only
3. `payload["narrative_result_source"]` fingerprint

No Report Engine work. No Narrative Engine package edits in this integration layer.

---

## 4. Result Page audit — section consumption

Official path:

```
/analyze
  → data.narrative_result
  → adaptAnalysisToCanonicalDesktop (narrativeResult + S01/S08/S11 prefer Pack 05)
  → adaptResultPageViewModel (interpretation + recommendations prefer Pack 05)
  → Result zones / cards
```

| Zone / card | Pack 05 preference | Notes |
|-------------|-------------------|--------|
| Executive (via S08 → Result VM) | Yes (via `mapS08`) | Summary identity / strengths / weaknesses / actions |
| Hero / S01 decisions | Yes (via `mapS01`) | Identity / strengths / priority recommendation |
| Closing / S11 | Yes (via `mapS11`) | Conclusion paragraphs + recommendations |
| Recommendation zone (LP-005) | Yes | `resultPresentationAdapter.buildRecommendations` |
| Interpretation zone (LP-006) | Yes | `buildInterpretation` from roles / summary |
| Knowledge zone (LP-007) | Structural (chart facts) | Not prose narrative; uses pattern/score slices |
| Chart / Score / Pattern / ShenSha / Feng Shui cards | Engine facts | Out of narrative scope |
| BaZi Result screen (parallel) | Yes | `baziResultAdapter.mapInterpretation` prefers Pack 05 |

Legacy `interpretation.sections` are used **only** when `narrative_result` is missing or unusable. Rule-prose continues to be gated by `commercialOrUnavailable` / `UNAVAILABLE_CONCLUSION`.

---

## 5. Portal official consumer

| File | Change |
|------|--------|
| `adapters/narrativeResultAdapter.ts` | DTO helpers (`asNarrativeResult`, `hasUsableNarrativeResult`, role/section helpers) |
| `adapters/canonicalDesktopAdapter.ts` | `narrativeResult` on VM; S01 / S08 / S11 prefer Pack 05 |
| `adapters/baziResultAdapter.ts` | Interpretation paragraphs prefer Pack 05 |
| `screens/result/adapters/resultPresentationAdapter.ts` | Recommendations + interpretation blocks prefer Pack 05 |
| `models/dto.ts` | `narrative_result?: Record<string, unknown>` |
| `adapters/index.ts` | Export narrative helpers |

---

## 6. Duplicate ViewModels / adapters

**Not deleted** in this epic (still referenced by screens/tests):

- `BaZiResultViewModel` / `BaZiResultScreen` / `useBaZiResult` — parallel Wave-3 screen; now Pack 05–aware
- WP-0004 Executive Summary / WP-0009 Consultation Report ViewModels — separate Pack 06 screens, not Result Page path
- `data.narrative` delivery adapter path — Report delivery BC

Deletion of parallel stacks is deferred to **Remaining Gaps** (unsafe while screens remain mounted).

---

## 7. Tests executed

| Suite | Result |
|-------|--------|
| `pytest applications/api/tests/test_product_integration_v1_narrative_result.py -q` | **1 passed** |
| `npm run typecheck` (customer_portal) | **pass** |
| `vitest run tests/js/canonical_desktop_adapter.test.tsx` | **4 passed** |

Did **not** run full-project pytest (per testing rules).

---

## 8. Files changed (this epic — product integration)

### Added
- `applications/api/services/narrative_result_truth.py`
- `applications/api/tests/test_product_integration_v1_narrative_result.py`
- `applications/customer_portal/src/adapters/narrativeResultAdapter.ts`
- `knowledge/architecture/pack_05_narrative_engine/reports/PRODUCT_INTEGRATION_V1_REPORT.md`
- `knowledge/architecture/pack_05_narrative_engine/reports/PRODUCT_INTEGRATION_V1_REMAINING_GAPS.md`

### Modified
- `applications/api/services/orchestrator.py`
- `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts`
- `applications/customer_portal/src/adapters/baziResultAdapter.ts`
- `applications/customer_portal/src/adapters/index.ts`
- `applications/customer_portal/src/models/dto.ts`
- `applications/customer_portal/src/screens/result/adapters/resultPresentationAdapter.ts`
- `applications/customer_portal/tests/js/canonical_desktop_adapter.test.tsx`

### Explicitly not modified
- Foundation / Design System / Visual Language
- Report Engine
- Narrative Engine internals (integration consumes public API only)
- Golden Dataset / snapshots / expected fixtures under `knowledge/golden_dataset`

---

## 9. Verdict

**Portal Result Page is the official consumer of Pack 05 `NarrativeResult`.**  
Legacy interpretation remains on the wire for backward compatibility and fallback only. Remaining parallel screens and delivery naming are tracked in the gap report.
