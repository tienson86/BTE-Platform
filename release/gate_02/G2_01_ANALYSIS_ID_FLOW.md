# G2-01 — Analysis ID flow

## Authoritative chain (production HTML Portal)

```
Birth form
  → POST /backend/api/v1/analyze
  → FastAPI APIResponse { data, request_id }
  → analyze.js keeps only { input, data }   // envelope request_id DROPPED
  → ResultStore.save
       write bte_last_result
       makeAnalysisId(result):
         result.analysis_id | result.id
         | data.analysis_id | data.request_id | data.case_id
         | "bte-{y}-{m}-{d}-{h}-{min}-{Date.now()}"
       write bte_current_analysis_id
       append bte_history row with that id
       clear bte_view_result
  → GET /result
       resolveForDisplay(from=history?)
       buildFullReportViewModel(..., analysisId)
       s00.chartId = that id
       data-analysis-id on ResultPageBody
```

Live orchestrator payloads have **`analysis_id: null`**. Envelope `request_id` is the only UUID from the API and is **not stored**.

## Field table

| Field | Created where | Stored where | Consumed where | Canonical? | Legacy? |
|-------|---------------|--------------|----------------|------------|---------|
| API `request_id` | middleware on POST /analyze | API envelope only | PortalApp `resolveAnalysisId` (non-prod SPA) | **Should be** public id | unused by HTML Analyze |
| `data.analysis_id` | not published by orchestrator | — | `analysisIdOf`, `sanitizeAnalysisId` | unused | — |
| `bte_current_analysis_id` | ResultStore.save `makeAnalysisId` | session + local | `loadCurrent`, Reports current row, Full Report | **de facto current** | synthetic |
| History `id` / `analysis_id` | `historyRow` copies current id | `bte_history[]` | History/Reports open | per-record | same synthetic family |
| `bte_view_analysis_id` | `selectForView` | session only | `resolveForDisplay(true)` | history view | — |
| `s00.chartId` | adapter from boot `requestId` | not persisted separately | Technical Information | display copy | fixture if missing |
| `data-analysis-id` | ResultPageBody | DOM | audit/CSS only | display copy | — |
| `chart_id` | not a production ResultStore key | — | — | no | — |
| `customer.customer_id` | optional birth field | inside `data.customer` | S00 fallback after requestId | not analysis id | — |
| Report V1 metadata analysis id | ReportInput adapter (server export) | export files | PDF/DOCX ops path | **separate** from Portal store | not customer |

## Canonical identity (as implemented)

**De facto:** `bte_current_analysis_id` after a successful Analyze.

**Not:** API `request_id` (dropped). **Not:** a server analysis record. **Not:** History index.

Consequence: two Analyzes of the same birth get different IDs (`Date.now()`). Refresh keeps the same stored id. Backend restart does not change the stored blob.

## Intended vs actual (History)

| Action | last_result | view | /result no query | /result?from=history | refresh |
|--------|-------------|------|------------------|----------------------|---------|
| Analyze C | C | cleared | C | C (view empty → current) | C |
| Open History B | still C | B (session) | C | B | B if URL still `from=history` and session view intact; else C |
| Analyze after viewing B | new D | cleared | D | D | D |
