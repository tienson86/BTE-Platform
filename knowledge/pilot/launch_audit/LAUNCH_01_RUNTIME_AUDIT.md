# LAUNCH-01 — Runtime Launch Gap Audit

**Task:** BTE LAUNCH-01  
**Scope:** Diagnostic only — no production code changes  
**Date:** 2026-08-12  
**Target journey:** User birth data → analysis request → canonical pipeline → report → public API → Portal Result Viewer → Result V2  

---

## 1. Executive Summary

The production host `applications.api.app:app` can already run a **real** end-to-end BaZi chart via `POST /api/v1/analyze` → `OrchestratorService.analyze()` (Calendar → BaZi → Pattern → Score → Interpretation → Report → Narrative), including Pack 05 `narrative_result`.

The Portal commercial journey that mounts Result V2 **does not call that API**. The analysis wizard only navigates locally; `ResultViewerPage` hard-wires `portalDemoReport`. Result V2 itself works when given a `CanonicalReportInput` with a `presentation` envelope, but **no runtime adapter** maps `/api/v1/analyze` (or report pipeline) output into that envelope.

`UnboundPipelineGateway` is the default for the optional Beta-2 `ServiceRegistry` public service layer (`POST /api/v1/analysis`). That layer is **not mounted** on the current production app. It is not the binding used by the live Portal client path (`POST /api/v1/analyze`).

**Verdict:** Backend one-chart path is largely ready; Portal → Result V2 launch path is partially connected and blocked by missing submission + missing presentation adaptation.

---

## 2. Current Runtime Path

### 2.1 Production path used by Portal client contracts

```
BirthRequest (year/month/day/…)
  → POST /api/v1/analyze          (applications/api/routes/v1.py)
  → OrchestratorService.analyze() (applications/api/services/orchestrator.py)
  → engines (Calendar…Report/Delivery)
  → APIResponse { success, data: { pipeline, bazi, …, report, narrative, narrative_result } }
```

Portal `AnalyzeService` targets this path (`API_ENDPOINTS.analyze` → `/analyze` under base `/api/v1`).

### 2.2 Alternate frozen public analysis endpoint (also mounted)

```
AnalyzeRequest
  → POST /analysis                (applications/api/routers/analysis.py)
  → DefaultAnalysisService
  → AnalysisAdapter / InterpretationAdapter / ReportAdapter
  → OrchestratorService
  → ReportResponse (contracts/report_response.py)
```

### 2.3 Optional Beta-2 service layer (NOT mounted on production host)

```
AnalysisCreateRequest
  → POST /api/v1/analysis         (applications/api/v1/analysis.py)  ← not on app.py
  → applications.services.AnalysisService
  → CanonicalPipelinePort
  → default UnboundPipelineGateway → execution: "not_bound"
```

### 2.4 Portal Result V2 commercial surface (current)

```
WizardDraft (local React state)
  → hash navigation only (no POST)
  → ResultViewerPage
  → portalDemoReport (fixture CanonicalReportInput)
  → ResultPageV2 → adaptPortalResult → PortalResultModel
```

---

## 3. API Status

| Item | Finding |
|------|---------|
| **Public analysis endpoint (Portal)** | `POST /api/v1/analyze` — **CONNECTED** to `OrchestratorService` |
| **Frozen root analysis** | `POST /analysis` — **CONNECTED** to `DefaultAnalysisService` → orchestrator |
| **Beta-2 resource API** | `POST /api/v1/analysis` — designed; **not mounted** on `applications.api.app:app` |
| **Request model (Portal path)** | `BirthRequest` in `applications/api/schemas/common.py` (`year`, `month`, `day`, optional `hour`/`minute`/`gender`/`timezone`/`full_name`/…) |
| **Response model (Portal path)** | `APIResponse` (`success`, `message`, `data`, `request_id`); `data` includes public pipeline stages + `narrative_result` |
| **Request model (root `/analysis`)** | `AnalyzeRequest` in `applications/api/contracts/analyze_request.py` |
| **Response model (root `/analysis`)** | `ReportResponse` in `applications/api/contracts/report_response.py` |
| **Runtime service binding (Portal path)** | `Depends(get_orchestrator)` → `OrchestratorService()` — **real engines** |
| **UnboundPipelineGateway?** | Default for `ServiceRegistry.create_default()` only. **Not** the binding for `/api/v1/analyze` or `/analysis` on the production host |
| **Missing wiring** | (1) Portal does not call the API; (2) no analyze→`CanonicalReportInput.presentation` bridge; (3) Beta-2 `/api/v1/analysis` remains unbound **if** that contract is chosen later |

OpenAPI confirmation (production app): `/api/v1/analyze` present; `/analysis` present; `/api/v1/analysis` **absent**.

---

## 4. Pipeline Status

| Item | Finding |
|------|---------|
| **Canonical analysis entry** | `OrchestratorService.analyze()` / `run_stage("analyze")` → stop at Delivery |
| **Required input** | `year`, `month`, `day`; optional `hour`, `minute`, `gender`, `timezone` |
| **Actual output** | Public payload: `calendar`, `bazi`, `pattern`, `score`, `interpretation`, `report`, `narrative`, plus `narrative_result` (Pack 05), strength/temperature/useful_god as published by stages |
| **Real chart execution?** | **Yes** — verified by existing integration tests |
| **Report generation connected?** | **Yes** — Stage 12 `ReportEngine.render_from_analysis`; Stage 13 delivery narrative |

Internal order (SSOT comment in orchestrator): Input → Calendar → BaZi → Feng Shui → Pattern → RuleContext → Score → Luck → Knowledge → Matching → Priority → Interpretation → Report → Delivery.

Public `data.pipeline` labels: `calendar → bazi → pattern → score → interpretation → report → narrative`.

**Note:** RX-1 `CanonicalReportPipeline` exists under `engines/report_engine/pipeline/` but is **not** the path invoked by `OrchestratorService`. Production analyze uses legacy `ReportEngine.render_from_analysis`.

---

## 5. Report Status

| Layer | Status |
|-------|--------|
| Orchestrator Stage 12–13 | **CONNECTED** — report + narrative views on analyze payload |
| `POST /api/v1/report` | **CONNECTED** — same orchestrator, stops before narrative |
| `ReportAdapter` / `DefaultReportService` | **CONNECTED** for root `/analysis` / report service deps |
| RX-1 Canonical Report Pipeline | **EXISTS** as engine module; **not wired** into Portal launch path |
| Result V2 `presentation` envelope on API | **MISSING** — analyze payload has no `presentation` field; Result V2 adapter requires it |

Pack 05 `narrative_result` is published on analyze and is what Canonical Desktop adapters consume — **not** what Result V2 `adaptPortalResult` consumes.

---

## 6. Portal Status

| Component | Location | Status |
|-----------|----------|--------|
| Analysis form | `features/portal/pages/AnalysisWizard.tsx` | UI collects draft; **no API submit** |
| Submission handler | Chart → Progress → Result navigation only | **MISSING** real submit |
| API client | `src/api/*`, `services/analyzeService.ts` | **CONNECTED** for Canonical Desktop / BaZi Result paths |
| Result Viewer | `features/portal/pages/ResultViewerPage.tsx` | **MOCKED** — `report={portalDemoReport}` |
| Portal shell routing | `features/portal/PortalApp.tsx` | Draft state held; never passed to Result Viewer as API result |
| Where real API data is expected | `AnalyzeService.analyze` → adapters for **Canonical Desktop / BaZi**, not Result V2 | Result V2 never receives live data |

Wizard “Bắt đầu phân tích” only calls `onNavigate("analyze-progress")`. Progress “Xem kết quả” only calls `onNavigate("result")`.

---

## 7. Result V2 Status

| Item | Finding |
|------|---------|
| **Expected model** | `PortalResultModel` (`bte.portal.result_ui.v2`) in `features/result_v2/adapter/PortalResultModel.ts` |
| **Adapter** | `adaptPortalResult(CanonicalReportInput)` in `portalPresentationAdapter.ts` |
| **Entry point** | `ResultPageV2` → `useResultPage` → `adaptPortalResult` → `ResultPage` |
| **Input contract** | `CanonicalReportInput` with required usable `presentation` (identity + summary bullets) |
| **Can real runtime output be adapted today?** | **No** — no mapper from analyze/`narrative_result`/RX-1 result → `CanonicalReportInput.presentation` |
| **Missing connection** | Portal must (a) call `/api/v1/analyze`, (b) map response → `CanonicalReportInput`, (c) pass into `ResultPageV2` instead of `portalDemoReport` |

Adapter behavior when `presentation` is absent: page state `empty` (confirmed by unit tests).

---

## 8. Mock/Demo Dependencies

| Asset | Role |
|-------|------|
| `features/portal/fixtures/demoReport.ts` (`portalDemoReport`) | **Hard dependency** of Result Viewer |
| `tests/js/result_v2_fixture.ts` | Test/screenshot fixture for Result V2 |
| `screens/bazi/mockData.ts`, `canonical_desktop/mockData.ts` | Alternate UIs / `BTE_DATA_SOURCE=mock` |
| `AnalyzeService` mock branch | Only when `isMockDataSource()` — not the Portal Result Viewer path |
| Wizard `INITIAL_DRAFT` | Pre-filled demo identity (“Nguyễn Văn An”) |

---

## 9. Exact First Broken Link

**First broken link (journey order):**

> Portal analysis wizard never POSTs birth data to `/api/v1/analyze` (or any analysis endpoint).  
> File: `applications/customer_portal/src/features/portal/pages/AnalysisWizard.tsx`  
> (`ChartInputPage` / `AnalysisProgressPage` are navigation-only.)

Immediately downstream of that:

> `ResultViewerPage` ignores draft/API and always renders `portalDemoReport`.  
> File: `applications/customer_portal/src/features/portal/pages/ResultViewerPage.tsx`

Even after wiring submit + viewer props, a second structural gap remains:

> No runtime adapter from analyze payload → `CanonicalReportInput.presentation` for Result V2.

---

## 10. Minimal Fix Sequence

1. **Wire Portal submit** — From wizard draft, build `AnalyzeChartRequest` and call `AnalyzeService.analyze` (or equivalent) on “Bắt đầu phân tích” / progress step.
2. **Hold result state** — Store `APIResponse.data` (and request metadata) in PortalApp (or a thin result store); pass into Result Viewer.
3. **Add presentation bridge** — Map analyze/`narrative_result` (and customer echo) → `CanonicalReportInput` with `presentation` envelope required by `adaptPortalResult`. Keep Result V2 adapter unchanged.
4. **Replace demo binding** — `ResultViewerPage` accepts `report: CanonicalReportInput` from live state; keep `portalDemoReport` only for preview/tests.
5. **Do not block on Beta-2 UnboundPipelineGateway** for this launch path — production Portal already targets `/api/v1/analyze`. Binding `CanonicalPipelinePort` is a separate host concern if `/api/v1/analysis` is adopted later.
6. **Smoke one real chart** — Birth data → Result V2 ready/partial_ready with non-demo hero name.

---

## 11. Files Expected To Change

*(LAUNCH-02+; not changed in this audit)*

- `applications/customer_portal/src/features/portal/pages/AnalysisWizard.tsx`
- `applications/customer_portal/src/features/portal/PortalApp.tsx`
- `applications/customer_portal/src/features/portal/pages/ResultViewerPage.tsx`
- New or existing Portal adapter: analyze/`narrative_result` → `CanonicalReportInput` (likely under `features/portal/` or `features/result_v2/adapter/`, without redesigning Result V2 components)
- Portal tests covering submit → Result V2 ready path

Optional later (only if product chooses Beta-2 resource API):

- Host binding implementing `CanonicalPipelinePort` → `OrchestratorService`
- Mount `register_public_service_layer` **or** replace unbound default at host composition root

---

## 12. Files That MUST NOT Change

Per LAUNCH-01 constraints (and for LAUNCH-02 unless explicitly rescoped):

- Engines (`engines/**`)
- Knowledge Packages
- Canonical pipeline stage semantics inside `OrchestratorService` (no redesign)
- Foundation / AF-1
- Existing API contracts for `/api/v1/analyze` request/response shape (additive fields only if unavoidable)
- Result V2 UI contract / component redesign (`PortalResultModel` semantics)
- Portal chrome redesign beyond wiring
- Strength calibration / Golden Dataset
- New database, analytics, authentication

---

## 13. Recommended LAUNCH-02

**LAUNCH-02 — Wire one real chart into Portal Result V2**

Goal: One user-entered birth chart appears in Result V2 via live `POST /api/v1/analyze`, with a thin presentation mapper and no engine/pipeline redesign.

Acceptance sketch:

1. Wizard submit calls `/api/v1/analyze` with real draft fields.
2. Result Viewer renders `ResultPageV2` from mapped live `CanonicalReportInput` (not `portalDemoReport`).
3. Hero/summary reflect runtime/`narrative_result` content for that birth data.
4. Lightweight tests: mapper unit test + one Portal integration (mocked fetch OK) + reuse existing API analyze test.

---

## 14. Validation Plan

### Tests executed for this audit

| Test | Result |
|------|--------|
| `applications/api/tests/test_product_integration_v1_narrative_result.py` | **PASSED** (1) — real `OrchestratorService.analyze` publishes Pack 05 `narrative_result` |
| `applications/api/tests/test_integration_api.py::test_analyze_end_to_end` | **PASSED** — HTTP `POST /api/v1/analyze` full public pipeline |
| `applications/api/tests/test_integration_api.py::test_openapi_lists_all_endpoints` | **PASSED** — `/api/v1/analyze` listed |
| `applications/customer_portal` vitest `tests/js/result_v2_adapter.test.ts` | **PASSED** (5) — adapter maps presentation; empty without presentation |

### Runtime checks (manual/script)

- `ServiceRegistry.create_default().pipeline` → `UnboundPipelineGateway` (`execution: not_bound`, `bound: False`)
- Production OpenAPI: `/api/v1/analyze` and `/analysis` present; `/api/v1/analysis` **not** present

### Scope gate

```
git diff --name-only
```

Expected: only `knowledge/pilot/launch_audit/LAUNCH_01_RUNTIME_AUDIT.md` (new). No tracked production modifications.

### Post–LAUNCH-02 validation (recommended)

1. Repeat `test_analyze_end_to_end` (unchanged).
2. Mapper unit: sample analyze DTO → `adaptPortalResult` → `page.state` in `{ready, partial_ready}`.
3. Manual: enter non-demo birth data → Result V2 hero name ≠ fixture “Nguyễn Văn An” unless that was the typed name.

---

## One-real-chart path status matrix

| Stage | Status |
|-------|--------|
| birth data (Portal form collection) | **PARTIAL** |
| → API (`POST /api/v1/analyze`) | **MISSING** (Portal never calls) / endpoint itself **CONNECTED** |
| → analysis (`OrchestratorService`) | **CONNECTED** |
| → report (orchestrator Stage 12–13) | **CONNECTED** |
| → adapter (analyze → `CanonicalReportInput`) | **MISSING** |
| → Portal Result Viewer | **MOCKED** |
| → Result V2 (`ResultPageV2` + `adaptPortalResult`) | **CONNECTED** (given fixture/`CanonicalReportInput`) |

Parallel note: Beta-2 `CanonicalPipelinePort` default = **UNBOUND** (not on production Portal path).

---

LAUNCH_PATH_STATUS: PARTIALLY_CONNECTED

NEXT_TASK: LAUNCH-02
