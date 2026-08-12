# LAUNCH-08 — Real Multi-Chart Beta Acceptance

**Task:** BTE LAUNCH-08  
**Date:** 2026-08-12  
**Scope:** ACCEPTANCE / VALIDATION only — no UI redesign, no engine/API/Knowledge changes  

---

## 1. Objective

Validate that Portal → `POST /api/v1/analyze` → OrchestratorService → `liveAnalysisResultAdapter` → PortalResultModel → Result V2 can reliably display **eight different** owner-verified real BaZi charts — not only the Nguyen Tien Son baseline.

---

## 2. Case Matrix

| Case | API | Adapter | Result V2 | Subject | Pillars | Fundamentals | Narrative | Empty Domain Handling | Demo Fallback | Runtime Error | Verdict |
|------|-----|---------|-----------|---------|---------|--------------|-----------|-----------------------|---------------|---------------|---------|
| CASE-001 Nguyen Tien Son | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS (none) | PASS (none) | **PASS** |
| CASE-002 Dinh Thanh Trung | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS (none) | PASS (none) | **PASS** |
| CASE-003 Nguyen Tien Khang | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS (none) | PASS (none) | **PASS** |
| CASE-004 Nguyen Tien Minh | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS (none) | PASS (none) | **PASS** |
| CASE-005 Luong Ngoc Huynh | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS (none) | PASS (none) | **PASS** |
| CASE-006 Nguyen Thi Huong Mai | PASS | PASS | PASS | PASS | **PARTIAL** | PASS | PASS | PASS | PASS (none) | PASS (none) | **PASS_WITH_ISSUES** |
| CASE-007 Vu Thi Thanh Tuyen | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS (none) | PASS (none) | **PASS** |
| CASE-008 Cao Anh Cuong | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS (none) | PASS (none) | **PASS** |

**CASE-006 Pillars PARTIAL — DISCREPANCY (not patched):**

| Pillar | Owner verified | Runtime |
|--------|----------------|---------|
| Year | Mau Thin | Mậu Thìn — match |
| Month | **Dinh Ty** | **Mậu Ngọ** — **DISCREPANCY** |
| Day | Quy Ty | Quý Tỵ — match |
| Hour | Nham Tuat | Nhâm Tuất — match |

Engine was **not** modified to force a match.

---

## 3. API Results

**REAL_RUNTIME_REPLAY:** AVAILABLE (local FastAPI `TestClient` → `applications.api.app:create_app()` → `POST /api/v1/analyze` → OrchestratorService)

Captured fixtures:

`applications/customer_portal/src/features/portal/fixtures/launch_08/case_00N_response.json`

| Case | HTTP | success | request_id | pipeline |
|------|------|---------|------------|----------|
| 001 | 200 | true | `launch08-case-001-nguyen-tien-son` | calendar→…→narrative |
| 002 | 200 | true | `launch08-case-002-dinh-thanh-trung` | same |
| 003 | 200 | true | `launch08-case-003-nguyen-tien-khang` | same |
| 004 | 200 | true | `launch08-case-004-nguyen-tien-minh` | same |
| 005 | 200 | true | `launch08-case-005-luong-ngoc-huynh` | same |
| 006 | 200 | true | `launch08-case-006-nguyen-thi-huong-mai` | same |
| 007 | 200 | true | `launch08-case-007-vu-thi-thanh-tuyen` | same |
| 008 | 200 | true | `launch08-case-008-cao-anh-cuong` | same |

All eight produce a real `analysisResult` with `bazi`, `pattern`, `strength`, `score`, `narrative_result`.

---

## 4. Adapter Results

For every case: `adaptLiveAnalysisResult(...)` → **`ok: true`**

- Subject identity mapped  
- Technical pillars + day master / pattern / strength metadata mapped when present  
- Seven narrative sections → `presentation.knowledge`  
- Career assessment mapped without remounting narrative sections  
- Empty wealth/relationship/health/luck remain unavailable  

`adaptPortalResult` → valid `PortalResultModel` (`partial_ready` or `ready`) for all eight.

---

## 5. Result V2 Results

Deterministic Portal render (`ResultViewerPage`) for each fixture:

| Check | Result |
|-------|--------|
| Renders without exception | PASS (8/8) |
| `data-analysis-source="api"` | PASS |
| `data-result-map="api"` | PASS |
| Correct subject name | PASS |
| Seven section titles visible | PASS |
| Demo subject / demo headline absent | PASS |

---

## 6. Chart Fundamental Variation

| Case | Day Master | Pattern (runtime) | Strength label | Strength score | Score grade |
|------|------------|-------------------|----------------|----------------|-------------|
| 001 | Canh | Chính Ấn | Thân vượng | 0.87 | D+ |
| 002 | Bính | Thiên Ấn | Thân vượng | 0.89 | D+ |
| 003 | Nhâm | Tòng Nhi cách — … | Thân vượng | 0.66 | D+ |
| 004 | Mậu | Thực Thần sinh Tài — … | Thân vượng | 0.84 | D+ |
| 005 | Bính | Chính Tài | Thân vượng | 0.66 | D+ |
| 006 | Quý | Thiên Tài | Trung hòa | 0.50 | D |
| 007 | Mậu | Tòng Tài cách — … | Thân vượng | 0.76 | D+ |
| 008 | Ất | Thiên Tài | Trung hòa | 0.46 | (empty) |

**Variation:** names, pillars, day masters, patterns, and strength scores differ across charts.  
**No cross-chart contamination** of another chart’s pillars/name/id.

**UPSTREAM_CONTENT_REUSE:** strength label string `"Thân vượng"` appears on multiple strong charts (001–005, 007). Displayed as supplied — not patched.

Strength astrology correctness was **not** judged (Pilot calibration separate).

---

## 7. Narrative Variation

| Check | Result |
|-------|--------|
| Seven sections present when supplied | PASS (8/8) |
| Section order preserved | PASS |
| First-section body differs across charts | PASS (set size > 1) |
| Associated with correct subject | PASS |
| Not replaced by demo | PASS |
| Portal duplicate of seven sections into career | PASS (absent) |

Commercial/upstream ellipsis quality remains an upstream concern (LAUNCH-07).

---

## 8. Empty Domain Validation

For all eight live models:

| Domain / zone | Rendered empty? |
|---------------|-----------------|
| wealth | Hidden |
| relationship | Hidden |
| health | Hidden |
| luck | Hidden |
| charts | Empty / hidden |
| appendix | Null / hidden |
| knowledge | **Mounted with real seven sections** (not fake filler) |

---

## 9. Demo Isolation

Every live case:

- `data-analysis-source="api"`  
- Demo identity `Nguyễn Văn An` absent  
- `portalDemoReport` headline absent  

Separate demo render still uses `data-analysis-source="demo"`.

---

## 10. Duplicate Rendering

| Risk | Result |
|------|--------|
| Narrative remounted inside career detail | Not present |
| Primary recommendation duplicated as domain card | Not present (`recommendation_ids=[]`) |
| Same subject/pillars for every chart | Fail if occurred — **did not occur** |

---

## 11. Runtime Errors

No Result V2 runtime errors observed in the deterministic acceptance suite (64 portal/Result V2 tests green including 28 LAUNCH-08 tests).

---

## 12. Browser Availability

**BROWSER_VALIDATION:** NOT_AVAILABLE

No browser harness was run. Validation is API capture + Portal/Result V2 unit/integration under Vitest.

---

## 13. Overall Acceptance

### Decision: **PASS_WITH_ISSUES**

**Why not FAIL:** All eight charts produce successful API → adapter → Result V2 paths with correct subject isolation, narrative, fundamentals, empty-domain handling, and no demo fallback.

**Why not PASS:** CASE-006 month pillar **DISCREPANCY** vs owner-verified fixture (runtime Mậu Ngọ vs verified Dinh Ty). Recorded only; engine not changed.

---

## 14. Failures / Discrepancies

1. **CASE-006 month pillar DISCREPANCY** — owner fixture vs Orchestrator runtime (see §2).  
2. **UPSTREAM_CONTENT_REUSE** — repeated `"Thân vượng"` strength label across multiple strong charts.  
3. **CASE-008 score grade empty** in capture — displayed as available fields only; no fabricated grade.  
4. Browser UX not validated.

---

## 15. Recommended LAUNCH-09

1. Investigate CASE-006 month-pillar discrepancy with calendar/hour-boundary owners (do not force-fit in UI).  
2. Optional private beta checklist / consultant walkthrough of the eight fixtures.  
3. Upstream narrative/strength-label quality (content reuse / ellipsis) if commercial polish is required.  
4. Browser harness screenshots only if a real browser path is later enabled.

---

## Tests / TypeScript / Scope

```text
npx vitest run src/features/portal
# (+ Result V2 adapter/page tests)
npx tsc --noEmit
```

Fixtures + tests under `applications/customer_portal/**` only.  
This audit: `knowledge/pilot/launch_audit/LAUNCH_08_MULTI_CHART_ACCEPTANCE.md`.

---

LAUNCH_08_STATUS: COMPLETE

NEXT_TASK: LAUNCH-09
