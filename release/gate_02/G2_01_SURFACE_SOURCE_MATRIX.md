# G2-01 — Surface / source matrix

Production host: FastAPI `applications.customer_portal.app` (port 8081).  
Not production: React `PortalApp` hash SPA (`portalScreenshotApp.tsx`, Vitest only).

| Surface | Route / component | Data source | Adapter | Analysis ID source | Fallback source | Legacy dependency | Customer-visible? |
|---------|-------------------|----------------|---------|--------------------|-----------------|-------------------|-------------------|
| Birth Input / Analyze | `GET /analyze` + `static/js/analyze.js` | POST `/backend/api/v1/analyze` → orchestrator | none (stores raw `data`) | ResultStore `makeAnalysisId` after save (not API `request_id`) | form validation only | none | **Yes** |
| Canonical /result | `GET /result` → `result_desktop.html` + `static/dist/result.js` | ResultStore `resolveForDisplay(fromHistory)` | `adaptAnalysisToCanonicalDesktop` → `adaptResultPageViewModel` | `fullReport.analysisId` / `s00.chartId` | mock fixture if store empty (`previewFallback: true`) | `bte_portal_last_result` read if new key missing | **Yes — canonical** |
| Technical Information | Result Context zone / S00 | same stored `data` | `mapS00` | `s00.chartId` | fixture chartId if no requestId | mock S00 fields | **Yes** |
| Luận giải | `/result#interpretation` or `GET /interpretation` (same desktop template) | **same** ResultStore payload | Interpretation zone from NarrativeResult | same `model.analysisId` | legacy `data.interpretation` sections only if NarrativeResult absent | `BaZiResultScreen` `#luan-giai` not mounted on /result | **Yes** |
| Full Report HTML (in /result print) | `#xuat` → `window.print()` | `buildFullReportViewModel(data)` from boot | `fullReportViewModel.ts` | sanitized analysis id | none if structured data present | none | **Yes** |
| Báo cáo / Reports | `GET /reports` + `reports.js` + `static/dist/report.js` | History list + `bte_last_result` | `BteFullReport.build/render` | report.id / `getCurrentAnalysisId` | `report.html` / executive presenters if unstructured | `presenters/executive.js` | **Yes** |
| Browser Print → PDF | `/result` or `/reports` print | same HTML as above | browser print | same | mock if empty result | not Report V1 PDF | **Yes** |
| Report V1 PDF | `ReportExportServiceV1.export_pdf` | server `ReportInputV1` from engines | Playwright/PDF exporter | report metadata | n/a | **not** wired to a Portal button | **No** (ops/validation) |
| DOCX | `ReportExportServiceV1.export_docx` | same ReportInputV1 | DOCX exporter | report metadata | n/a | **no Portal download** | **No** |
| History | `GET /history` + `history.js` | `bte_history` | `selectForView` | `item.analysis_id \|\| item.id` | empty state | `bte_portal_history` | **Yes** |
| History open | `/result?from=history` | `bte_view_result` (session) | same Canonical Desktop | `bte_view_analysis_id` | current last_result if view missing | loadForView on legacy page | **Yes** |
| Dashboard recent | `GET /dashboard` | history slice | `selectForView` | history id | — | — | **Yes** |
| Reload /result | same /result | session+local `bte_last_result` | same | `bte_current_analysis_id` | mock if keys gone | legacy last key | **Yes** |
| Direct /result | no query | `resolveForDisplay(false)` = current | same | current id | mock | view key ignored unless `?from=history` | **Yes** |
| Legacy result | `/result?legacy=1` | `loadForView()` = view **or** last | `static/js/result.js` + presenters | implicit | empty copy | **ACTIVE explicit** | Yes if URL used |
| PortalApp Result V2 | `#/result` (not served by portal app.py) | in-memory `analysisSession` | `adaptLiveAnalysisResult` → Result V2 | `response.request_id` | **demo report** if no id | `portalDemoReport` | Tests/screenshots only |
