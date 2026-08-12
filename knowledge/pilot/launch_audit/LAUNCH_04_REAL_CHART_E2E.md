# LAUNCH-04 — Real Chart End-to-End Validation

**Task:** BTE LAUNCH-04  
**Date:** 2026-08-12  
**Scope:** Integration validation only — no engine/API/UI redesign  

---

## 1. Test subject

| Field | Value |
|-------|--------|
| Name | Nguyen Tien Son |
| Gender | male |
| Gregorian birth | 1987-01-21 |
| Birth time | 04:30 |
| Birth place | Ha Noi, Vietnam |

**User-verified Four Pillars (fixture — not modified):**

| Pillar | Verified (ASCII) |
|--------|------------------|
| Year | Binh Dan |
| Month | Tan Suu |
| Day | Canh Ngo |
| Hour | Mau Dan |

---

## 2. Input data

```json
{
  "year": 1987,
  "month": 1,
  "day": 21,
  "hour": 4,
  "minute": 30,
  "gender": "male",
  "timezone": "Asia/Ho_Chi_Minh",
  "full_name": "Nguyen Tien Son",
  "birth_place": "Ha Noi, Vietnam"
}
```

Submitted to: `POST /api/v1/analyze`

---

## 3. API response status

| Check | Result |
|-------|--------|
| HTTP status | **200** |
| `success` | **true** |
| Orchestrator executed | **Yes** (`pipeline.start` → `pipeline.done stage=analyze`) |

**Command used (live capture):**

```text
PYTHONPATH=. python -c "<TestClient POST /api/v1/analyze via applications.api.app:create_app()>"
```

Capture written to:

`applications/customer_portal/src/features/portal/fixtures/launch_04_real_chart_response.json`

---

## 4. Analysis ID

`request_id` / analysis identifier:

**`launch04-nguyen-tien-son`**

(Header `X-Request-ID: launch04-nguyen-tien-son` echoed by API.)

---

## 5. Runtime structures observed

Public `data.pipeline`:

`calendar → bazi → pattern → score → interpretation → report → narrative`

Also present on payload:

- `customer` (name, place, gender, timezone)
- `bazi` (four pillars + day_master)
- `pattern` (e.g. Cách cục **Chính Ấn**)
- `score` (grade **D+**, total observed in logs ~51.25)
- `interpretation` (section_count=10)
- `report` / `narrative` (legacy delivery)
- `narrative_result` (`contract=pack05_narrative_result_v1`, `status=complete`, 7 sections, commercial executive + primary recommendation)

---

## 6. Adapter result

`adaptLiveAnalysisResult(analysisResult, { analysis_id })` → **`ok: true`**

Produced `CanonicalReportInput` with:

- `presentation.identity.full_name` = Nguyen Tien Son
- headline / one_line_summary from structured narrative executive fields
- summary bullets from live narrative strengths / executive points
- technical pillars + analysis id
- career primary recommendation when fully structured

---

## 7. PortalResultModel result

`adaptPortalResult(report)` → **success**

| Field | Observation |
|-------|-------------|
| `contract_id` | `bte.portal.result_ui.v2` |
| `hero.name` | Nguyen Tien Son |
| `page.state` | `ready` or `partial_ready` (not `error`) |
| `summary.bullets` | present (>0) |
| `technical.ids` | `launch04-nguyen-tien-son` |

---

## 8. Result Viewer result

`ResultViewerPage` with live session:

| Assertion | Result |
|-----------|--------|
| Runtime error / alert | **None** |
| Subject identity visible | **Nguyen Tien Son** |
| Demo identity absent | Nguyễn Văn An **not** shown |
| `data-result-map` | `api` |

---

## 9. Four Pillars verification

Runtime `bazi` pillars (Vietnamese):

| Pillar | Runtime | Folded ASCII | Verified fixture | Match |
|--------|---------|--------------|------------------|-------|
| Year | Bính Dần | binh dan | Binh Dan | **PASS** |
| Month | Tân Sửu | tan suu | Tan Suu | **PASS** |
| Day | Canh Ngọ | canh ngo | Canh Ngo | **PASS** |
| Hour | Mậu Dần | mau dan | Mau Dan | **PASS** |

Day master: **Canh** (consistent with day stem).

**No engine patch required. No discrepancy.**

---

## 10. Source verification

| Attribute | Value |
|-----------|--------|
| `data-analysis-source` | **`api`** |
| Demo fallback | **No** |
| `portalDemoReport` used | **No** (live path only) |

---

## 11. Optional data gaps (expected — not failures)

Per LAUNCH-03 / launch path:

- wealth / relationship / health / luck domains may be empty
- charts empty
- knowledge empty
- appendix empty
- root narrative recommendations without domain omitted (no invented domain)

---

## 12. Tests

| Suite | Result |
|-------|--------|
| `npx vitest run src/features/portal` | **18 passed** (includes LAUNCH-02/03/04) |
| Result V2 focused (`result_v2_adapter`, `result_v2_page`) | **7 passed** |
| Failures | **0** |

Focused file:

`applications/customer_portal/src/features/portal/launch_04_real_chart_e2e.test.tsx`

Covers:

1. API capture integrity  
2. Four Pillars vs verified fixture  
3. Live adapter success  
4. PortalResultModel success  
5. ResultViewer live render + `source=api`

---

## 13. TypeScript

`npx tsc --noEmit` → **exit 0**

---

## 14. Scope validation

`git diff --name-only` / untracked for this task limited to:

- `applications/customer_portal/**` (tests + live capture fixtures)
- `knowledge/pilot/launch_audit/LAUNCH_04_REAL_CHART_E2E.md`

No engines / pipelines / API production / Knowledge Packages / Foundation / AF-1 modifications.

---

## 15. Browser validation

Existing screenshot harnesses (`capture_result_v2_screenshots.mjs`, portal screenshot apps) drive **fixture/demo** Result V2 entries, not the live Nguyen Tien Son session, without changing application behavior.

**MANUAL_BROWSER_VALIDATION: NOT_AVAILABLE**

Automated Portal + Result V2 unit/integration path above remains the validation evidence.

---

## 16. Any discrepancy

**None.**

Four Pillars match the supplied verified fixture. Live adapter and Result V2 path succeeded with `source=api`.

---

## Success criteria checklist

| Criterion | Status |
|-----------|--------|
| Real chart submitted | PASS |
| Real API executed | PASS |
| Real analysis returned | PASS |
| Live adapter succeeded | PASS |
| PortalResultModel succeeded | PASS |
| Result V2 rendered (no runtime error) | PASS |
| `source=api` | PASS |
| No demo fallback | PASS |
| Four pillars match verified fixture | PASS |

---

LAUNCH_04_STATUS:
PASS

NEXT_TASK:
LAUNCH-05
