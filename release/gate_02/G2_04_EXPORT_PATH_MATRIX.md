# G2-04 — Export path matrix

Production host: FastAPI Customer Portal (`applications.customer_portal.app`, port 8081) proxying `POST /backend/api/v1/export/{pdf|docx}` to Applications API.

Canonical model: stored Analyze JSON → `build_customer_report_input` → `ReportInputV1` → `PresentedReportV1`.

| Surface | Customer action | Source object | Presentation builder | Renderer | Analysis ID | Contract | Customer accessible? | Canonical? | Legacy? |
|---------|-----------------|---------------|----------------------|----------|-------------|----------|----------------------|------------|---------|
| `/result` Full Report (on page) | Read Result cards | ResultStore selected `data` | `adaptResultPageViewModel` + `buildFullReportViewModel` | React Result UI | G2-01R `analysis_id` | `UsefulGodView@1.5` | Yes | **CANONICAL** Result | No |
| `/result` export bar | **Xem báo cáo** → `/reports` | Same stored `data` | Full Report VM | HTML preview | Same | `@1.5` | Yes | CANONICAL preview | No |
| `/result` export bar | **In** | Same Result DOM | Result print CSS | Browser print | Same | `@1.5` | Yes | **PRINT VIEW** | No |
| `/result` export bar | **Tải PDF** | Same stored `data` + `input` | `customer_report_input` → `PresentedReportV1` | Playwright Report V1 | Request + payload id | `@1.5` else 409 | Yes | **OFFICIAL PDF** | No |
| `/result` export bar | **Tải DOCX** | Same | Same `PresentedReportV1` | `DocxExporterV1` | Same | `@1.5` else 409 | Yes | **CANONICAL DOCX** | No |
| Sidebar “Xuất báo cáo” | Scroll to `#xuat` | — | — | — | — | — | Yes | Navigation only | No |
| `/reports` preview | Open / HTML tab | History or current stored row | `BteFullReport.build/render` | HTML | `currentAnalysisId` | `@1.5` notice if stale | Yes | CANONICAL on-screen | Unstructured HTML is EXPLICIT LEGACY |
| `/reports` | **In** | Preview HTML | Browser print | Print | Selected row | Same | Yes | PRINT VIEW | No |
| `/reports` | **Tải PDF** | Selected row `data` | Same official path | Playwright | Selected id | `@1.5` | Yes | OFFICIAL PDF | No |
| `/reports` | **Tải DOCX** | Selected row `data` | Same | python-docx | Selected id | `@1.5` | Yes | CANONICAL DOCX | No |
| Browser Print → Save as PDF | OS print dialog | Result or Reports HTML | Browser | Browser PDF | Same as view | Same as view | Yes | PRINT VIEW, not official | No |
| `POST /api/v1/export/pdf` | Download | Request body `data` | `PresentedReportV1` | Playwright | `analysis_id` + header | `@1.5` | Via Portal | **CANONICAL** | No |
| `POST /api/v1/export/docx` | Download | Request body `data` | `PresentedReportV1` | python-docx | Same | `@1.5` | Via Portal | **CANONICAL** | No |
| Report V1 HTML (`render_html`) | Internal / PDF source | `ReportInputV1` | `build_presented_report` | HTML string | `metadata.case_id` | Customer adapter | Indirect | **CANONICAL** source of official PDF | No |
| `ReportExportServiceV1` | Ops / tests | `ReportInputV1` | Same | PDF/DOCX | `case_id` | Report V1 | No (internal) | CANONICAL engine | INTERNAL ONLY |
| `CommercialPdfExporter` | Orchestrator leftover | Commercial builder | Commercial | PDF | n/a | n/a | No | No | **INTERNAL ONLY** |
| `engines/report_engine/simple_pdf.py` | Old helper | Markdown/HTML | Simple | PDF | n/a | n/a | No | No | **INTERNAL ONLY** |
| `word_renderer.py` / `markdown_renderer.py` | Old Report Engine | Report pipeline | Markdown/Word | File | n/a | n/a | No | No | **EXPLICIT LEGACY** |
| `/result?legacy=1` + `result.js` | Legacy result | `loadForView` | Presenters | HTML | Implicit | Unversioned | Only if URL used | No | **EXPLICIT LEGACY** |
| Reports “Tải xuống” HTML/MD of unstructured rows | Removed as official action | `report.html` / markdown | Local compose | Blob | Weak | None | No for fresh structured | No | **DEAD** for structured V1.0 |
| Mock BaZi “Xuất PDF — chưa khả dụng” | Sprint fixture | Mock | None | None | None | None | Tests only | No | **DEAD** product path |
| PortalApp hash SPA | Vitest / screenshots | In-memory | Result V2 | React | `request_id` | Demo | No (not served by portal app) | No | INTERNAL / tests |

## Classification summary

| Class | Paths |
|-------|--------|
| **CANONICAL** | Result UI, Full Report preview, official Playwright PDF, python-docx, shared `PresentedReportV1` |
| **PRINT VIEW** | `/result` In, `/reports` In, OS Print-to-PDF |
| **EXPLICIT LEGACY** | `/result?legacy=1`, old Word/Markdown renderers, unstructured stored `report.html` |
| **INTERNAL ONLY** | `ReportExportServiceV1` default export root, commercial/simple PDF helpers |
| **DEAD** | Dual “Xuất PDF” buttons, HTML/MD download as official customer file for structured `@1.5` results |

No unknown production export path remains for V1.0 Portal.
