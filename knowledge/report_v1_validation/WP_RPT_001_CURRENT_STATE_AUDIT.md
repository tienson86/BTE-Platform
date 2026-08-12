# WP-RPT-001 — Simple Report Export V1 Current State Audit

**Work Package:** WP-RPT-001 (READ-ONLY)  
**Branch audited:** `release/v1.0-final`  
**Audit date:** 2026-08-12  
**Auditor:** AI Agent (automated codebase inspection)

---

## 1. Executive Summary

BTE Platform đã có **~55–65% nền tảng** cần cho Simple Report Export V1:

| Layer | Readiness |
|-------|-----------|
| Pipeline đến Interpretation | **IMPLEMENTED** (OrchestratorService) |
| Report text/HTML cơ bản | **PARTIAL** (portal markdown/html từ interpretation sections) |
| Report Engine đầy đủ (templates, layout, rendering) | **PARTIAL** (code tồn tại, chưa wired vào production API) |
| PDF production | **PARTIAL** (simple_pdf Latin-1, không tiếng Việt đầy đủ) |
| DOCX production | **NOT IMPLEMENTED** (code legacy, dependency không có) |
| API export/download | **NOT IMPLEMENTED** (không có endpoint PDF/DOCX) |
| Frontend export | **PARTIAL** (print + HTML/MD blob; PDF/DOCX stub) |

### Câu trả lời ngắn

- **Có cần tạo Report Engine mới không?** **Không.** `engines/report_engine/` đã tồn tại với nhiều lớp (WP6 builder, RX-1 canonical pipeline, layout, rendering). WP-RPT-002 nên **mở rộng và nối** pipeline hiện có, không viết engine mới từ đầu.
- **Có thể tái sử dụng gì?** OrchestratorService, InterpretationResult (legacy runtime), portal_view serialization, ReportFormatter, simple_pdf, CanonicalReportPipeline, knowledge templates (`06_report_templates`), golden dataset harness, portal print CSS.
- **Blocker lớn nhất:** **Không có luồng end-to-end thống nhất** từ `InterpretationResult` → `ReportInputV1` → HTML chất lượng production → PDF/DOCX thật. Production hiện dùng `ReportEngine.render_from_analysis()` (markdown/html đơn giản), trong khi RX-1 pipeline và WP6 `build_full()` tồn tại song song nhưng không expose qua API/Portal.

**Recommendation status:** **READY WITH BLOCKERS**

---

## 2. Repository Components Found

| Component | Path | Status | Reusable |
|-----------|------|--------|----------|
| Report Engine (public API) | `engines/report_engine/` | IMPLEMENTED | Yes — primary target |
| ReportEngine class | `engines/report_engine/engine.py` | IMPLEMENTED | Yes |
| ReportService (WP6) | `engines/report_engine/service.py` | IMPLEMENTED | Yes |
| ReportBuilder + templates | `engines/report_engine/builder.py`, `knowledge_template_loader.py` | IMPLEMENTED | Yes |
| Canonical Report Pipeline (RX-1) | `engines/report_engine/pipeline/canonical_report_pipeline.py` | IMPLEMENTED | Yes — layout/rendering path |
| Layout Engine | `engines/report_engine/layout/` | IMPLEMENTED | Yes |
| Rendering Engine | `engines/report_engine/rendering/` | PARTIAL | Yes — PDF/DOCX are envelope stubs |
| ExportManager | `engines/report_engine/rendering/export_manager.py` | PARTIAL | Yes — dispatches stub renderers |
| simple_pdf (no deps) | `engines/report_engine/simple_pdf.py` | IMPLEMENTED | Yes — Latin-1 only |
| Legacy PDFRenderer (reportlab) | `engines/report_engine/pdf_renderer.py` | LEGACY | Conditional — reportlab not in requirements |
| Legacy WordRenderer (python-docx) | `engines/report_engine/word_renderer.py` | LEGACY | Conditional — python-docx not in requirements |
| Portal report view | `engines/report_engine/portal_view.py` | IMPLEMENTED | Yes — **production path** |
| Interpretation Engine | `engines/interpretation_engine/` | IMPLEMENTED | Yes |
| Runtime InterpretationResult | `engines/interpretation_engine/legacy_builder.py` | IMPLEMENTED (CANONICAL runtime) | Yes |
| Pack03 InterpretationResult | `engines/interpretation_engine/models/interpretation_result.py` | PARTIAL (architecture) | Future — not wired to orchestrator |
| Analysis Engine report_generator | `engines/analysis_engine/report_generator/` | LEGACY/PARALLEL | Partial — separate subsystem |
| Orchestrator (pipeline SSOT) | `applications/api/services/orchestrator.py` | IMPLEMENTED | Yes |
| API /api/v1/analyze | `applications/api/routes/v1.py` | IMPLEMENTED | Yes — primary endpoint |
| API POST /analysis | `applications/api/routers/analysis.py` | IMPLEMENTED | Yes — adapter contract |
| Public API /api/v1/analysis | `applications/api/v1/analysis.py` | STUB | No — UnboundPipelineGateway default |
| Customer Portal | `applications/customer_portal/` | IMPLEMENTED | Yes |
| Knowledge report templates (docs) | `knowledge/report_templates/` | DOC-ONLY | Spec reference |
| IE knowledge templates (runtime) | `engines/interpretation_engine/knowledge/06_report_templates/` | IMPLEMENTED | Yes — WP6 loader reads these |
| Golden dataset (operational) | `tests/golden_dataset/` | IMPLEMENTED | Yes |
| Golden dataset (framework) | `knowledge/golden_dataset/` | DOC-ONLY | Spec only |
| Pilot CASE-0001 | `knowledge/pilot/cases/CASE-0001/` | IMPLEMENTED | Yes — subject metadata |
| Playwright (QA only) | `validation/portal_qa_audit.py` | IMPLEMENTED | QA — not PDF export |
| Jinja2 templates | — | NOT IMPLEMENTED | No matches in codebase |

---

## 3. Current Report Engine Architecture

### 3.1 Directory Tree (summary)

```
engines/report_engine/
├── engine.py              # Public ReportEngine
├── service.py             # ReportService (WP6 build/format/export)
├── builder.py             # InterpretationResult → ReportModel
├── formatter.py           # TEXT / MD / HTML / JSON
├── portal_view.py         # Production portal dict (markdown/html)
├── simple_pdf.py          # Minimal PDF writer (no external deps)
├── pdf_renderer.py        # Legacy reportlab PDFRenderer
├── word_renderer.py       # Legacy python-docx WordRenderer
├── knowledge_template_loader.py
├── section_builders.py, section.py, report.py
├── content/               # Content engine (01–05 stages)
├── layout/                # Layout engine (RX-1 RE-2)
├── rendering/             # Rendering engine (RX-1 RE-3)
├── pipeline/              # CanonicalReportPipeline (RX-1)
├── integration/           # Foundation/Layout/Rendering stages
├── contracts/, context/, registry/, validation/
├── documentation/         # REPORT_FOUNDATION, LAYOUT, RENDERING, CANONICAL_PIPELINE
└── templates/default.md   # Legacy local template
```

### 3.2 Runtime Pipelines (multiple — important)

#### A. Production API path (active)

```
OrchestratorService._run()
  → InterpretationEngine.build_from_resolved()
  → build_interpretation_view()  [interpretation_truth.py]
  → ReportEngine.render_from_analysis(analysis)
      → build_report_portal_dict(interpretation)   [portal_view.py]
      → optional build_narrative_portal_dict()
  → build_report_view() / build_narrative_view()   [report_truth.py]
  → API payload: data.report { title, markdown, html, section_count }
```

**Classification:** IMPLEMENTED — but report is **thin** (sections → markdown/html strings, no full ReportModel).

#### B. WP6 full build path (tests / direct engine use)

```
InterpretationResult
  → ReportService.build() → ReportBuilder → KnowledgeTemplateLoader (06_report_templates)
  → ReportService.build_full()
      → formatter.to_markdown / to_html
      → write_simple_pdf() → reports/wp6_report.pdf
```

**Classification:** IMPLEMENTED — not wired to OrchestratorService or API.

#### C. RX-1 Canonical Report Pipeline (tests)

```
CanonicalReportPipeline.run(
    analysis_result, decision_result, luck_result, interpretation_result
)
  → FoundationStage → LayoutStage → RenderingStage
  → CanonicalReportResult (foundation + layout + rendering artifacts)
```

**Classification:** IMPLEMENTED in tests (`tests/report_engine/test_report_pipeline.py` — 58 tests pass).  
Rendering PDF/DOCX outputs are **JSON envelope stubs**, not binary files.

#### D. Legacy / parallel

| Module | Status |
|--------|--------|
| `engines/analysis_engine/report_generator/` | LEGACY — StructuredReport + serializers |
| `engines/report_engine/pdf_renderer.py` (reportlab) | LEGACY — requires reportlab |
| `engines/report_engine/word_renderer.py` (python-docx) | LEGACY — requires python-docx |
| `engines/interpretation_engine/renderer/` | LEGACY — Chapter-based PDF/DOCX |

### 3.3 Component Classification

| Component | Classification |
|-----------|----------------|
| ReportEngine.render_from_analysis | IMPLEMENTED (production) |
| ReportService.build_full | IMPLEMENTED (not production) |
| CanonicalReportPipeline | IMPLEMENTED (test/integration) |
| Layout Engine | IMPLEMENTED |
| Rendering Engine (HtmlRenderer) | PARTIAL (identity blocks, no CSS) |
| Rendering Engine (PdfRenderer, DocxRenderer) | STUB (JSON envelope) |
| PDFRenderer (reportlab) | LEGACY |
| WordRenderer (python-docx) | LEGACY |
| simple_pdf | IMPLEMENTED (minimal) |
| Knowledge templates 06_report_templates | IMPLEMENTED (WP6 loader) |
| knowledge/report_templates/ | DOC-ONLY |
| TemplateCoverageAnalyzer | IMPLEMENTED |

---

## 4. InterpretationResult Contract

### 4.1 Model Inventory

| Symbol | Path | Role |
|--------|------|------|
| **InterpretationResult** (runtime CANONICAL) | `engines/interpretation_engine/legacy_builder.py:228` | **Used by OrchestratorService, exported from `__init__.py`** |
| InterpretationResult (Pack03 frozen) | `engines/interpretation_engine/models/interpretation_result.py:14` | Architecture model — DUPLICATE / not orchestrator path |
| InterpretationResultModel | `engines/interpretation_engine/models/interpretation_result_model.py:10` | Architecture skeleton — DUPLICATE |
| InterpretationResult | `engines/analysis_engine/interpretation_engine/models.py:197` | LEGACY / analysis_engine copy — DUPLICATE |
| CanonicalInterpretationResult | `engines/interpretation_engine/contracts/interpretation_contracts.py` | Foundation contract — parallel track |

**Evidence for runtime canonical:** `applications/api/services/interpretation_truth.py` imports `from engines.interpretation_engine.legacy_builder import InterpretationResult`.

### 4.2 Runtime InterpretationResult Fields (legacy_builder)

```python
@dataclass
class InterpretationResult:
    summary: str
    sections: Dict[str, InterpretationSection]  # keyed by section id
    rules_used: List[str]
    strengths / weaknesses / warnings: List[Dict]
    confidence: float
    score: float
    sentences: List[Dict]
    matched_rule_count, sentence_count, section_count, coverage
    priority_resolution, resolved_rule_count, discarded_rules
    luck_context: Any | None  # not serialized to portal
```

**InterpretationSection** (per section): `id`, `title`, `content`, `score`, `rules`, etc.

### 4.3 Serialization Chain

```
InterpretationResult.to_portal_dict()
  → engines/interpretation_engine/portal_view.build_portal_dict()
build_interpretation_view(result)
  → InterpretationView (applications/api/models/analysis_result.py)
InterpretationView.to_dict()  → API data.interpretation
```

**Public API wire shape** (`InterpretationView.to_dict`):

```json
{
  "sections": [{"id", "title", "body"}],
  "section_count": int,
  "sentence_count": int,
  "confidence": float
}
```

**Stripped from API:** summary, matched_rule_count, coverage, metadata, priority_resolution, discarded_rules, unused_rules.

### 4.4 Pack03 Frozen Model (not production path)

`engines/interpretation_engine/models/interpretation_result.py`:

- `id`, `metadata`, `trace`, `source_final_result_id`, `pipeline_id`, `success`
- `sections: tuple[SectionResult, ...]`
- `explanation_refs`, `messages`, `attributes`

### 4.5 Missing Fields for Report Export V1

| Needed for Report | Available today | Gap |
|-------------------|-----------------|-----|
| Section prose | Yes (`body` per section) | OK |
| Subject name | BirthRequest.full_name (presentation only) | Not in InterpretationResult |
| Birth datetime | BirthRequest fields | Not in report payload |
| Chart/four pillars | BaziView on AnalysisResult | Report path ignores chart |
| Score/pattern summary | ScoreView, PatternView | Not in render_from_analysis |
| Brand/layout metadata | — | Missing |
| Template coverage | ReportModel.template_coverage | Only in WP6 path |

---

## 5. Current Runtime Sequence

### 5.1 Primary Production Path (`POST /api/v1/analyze`)

```
User Input (BirthRequest: year/month/day/hour/minute/gender/timezone)
  ↓
applications/api/routes/v1.py :: analyze_endpoint
  ↓
OrchestratorService.analyze() :: _run(stop_at="delivery")
  ↓
CalendarEngine.build → BaziEngine.build → PatternEngine → ScoreEngine
  → LuckEngine → Knowledge/Matching/Priority
  ↓
InterpretationEngine.build_from_resolved() → InterpretationResult
  ↓
build_interpretation_view() → InterpretationView
  ↓
build_narrative_result_dict() (Pack05 narrative, optional)
  ↓
ReportEngine.render_from_analysis(analysis)
  → build_report_portal_dict(interpretation) → {title, markdown, html, section_count}
  ↓
build_report_view() → ReportView.to_dict()
  ↓
APIResponse.data { bazi, pattern, score, interpretation, report, narrative, pipeline }
  ↓
Portal: POST /backend/api/v1/analyze → ResultStore → PortalPage / ResultPageV2
```

### 5.2 Test Trace (RX-1 pipeline — no HTTP)

```
tests/report_engine/test_report_pipeline.py :: test_normal_execution
  ↓
CanonicalReportPipeline.run(analysis, decision, luck, interpretation)
  ↓
FoundationStage → LayoutStage → RenderingStage
  ↓
CanonicalReportResult (success, foundation_result, layout_result, rendering_result)
```

Fixture inputs: `tests/report_engine/re2_support.py :: assemble_layout_inputs()`

---

## 6. API Inventory

### 6.1 Engine / Analysis Endpoints (`/api/v1/*`)

| Endpoint | Method | Handler | Input | Output | Status |
|----------|--------|---------|-------|--------|--------|
| `/api/v1/calendar` | POST | `calendar_endpoint` | BirthRequest | APIResponse (calendar) | IMPLEMENTED |
| `/api/v1/bazi` | POST | `bazi_endpoint` | BirthRequest | APIResponse (+bazi) | IMPLEMENTED |
| `/api/v1/pattern` | POST | `pattern_endpoint` | BirthRequest | APIResponse (+pattern) | IMPLEMENTED |
| `/api/v1/score` | POST | `score_endpoint` | BirthRequest | APIResponse (+score) | IMPLEMENTED |
| `/api/v1/interpretation` | POST | `interpretation_endpoint` | BirthRequest | APIResponse (+interpretation) | IMPLEMENTED |
| `/api/v1/report` | POST | `report_endpoint` | BirthRequest | APIResponse (+report) | IMPLEMENTED |
| `/api/v1/narrative` | POST | `narrative_endpoint` | BirthRequest | APIResponse (+narrative) | IMPLEMENTED |
| `/api/v1/analyze` | POST | `analyze_endpoint` | BirthRequest | APIResponse (full pipeline) | **PRIMARY — Portal uses this** |
| `/api/v1/discussion` | POST | `discussion_endpoint` | DiscussionRequest | APIResponse | IMPLEMENTED |

### 6.2 Public Contract Endpoints

| Endpoint | Method | Handler | Input | Output | Status |
|----------|--------|---------|-------|--------|--------|
| `/analysis` | POST | `routers/analysis.create_analysis` | AnalyzeRequest | ReportResponse | IMPLEMENTED (3× orchestrator runs) |
| `/api/v1/analysis` | POST | `v1/analysis.create_analysis` | AnalysisCreateRequest | PublicSuccessResponse | STUB (UnboundPipelineGateway) |
| `/api/v1/analysis/{id}` | GET | `v1/analysis.get_analysis` | id | PublicSuccessResponse | STUB |
| `/api/v1/report/{id}` | GET | `v1/report.get_report` | id | PublicSuccessResponse | STUB (retrieve by id) |

### 6.3 Case Export (not report PDF)

| Endpoint | Method | Handler | Input | Output | Status |
|----------|--------|---------|-------|--------|--------|
| `/api/v1/cases/{case_id}/export` | GET | `cases.export_case` | format=json\|markdown\|html | Response body | IMPLEMENTED — **no pdf/docx** |

### 6.4 Health / System

| Endpoint | Method | Status |
|----------|--------|--------|
| `/health`, `/api/v1/health`, `/live`, `/ready` | GET | IMPLEMENTED |
| `/version`, `/api/v1/version` | GET | IMPLEMENTED |

### 6.5 PDF / DOCX / Download Endpoints

**None found.** No `GET /report/{id}/pdf`, no `POST /export`, no binary download for DOCX.

### 6.6 Frontend API Usage

| Consumer | Endpoint | Evidence |
|----------|----------|----------|
| Legacy portal (`analyze.js`) | `POST /backend/api/v1/analyze` | `applications/customer_portal/static/js/analyze.js` |
| React Portal (`AnalyzeService`) | `POST /analyze` (via `API_ENDPOINTS`) | `src/services/analyzeService.ts` |
| Reports page | Local ResultStore history | `static/js/reports.js` — no server PDF |

---

## 7. Portal Integration

### 7.1 Applications

| App | Entry | Route |
|-----|-------|-------|
| FastAPI server | `applications/customer_portal/app.py` | `/analyze`, `/result`, `/reports` |
| Canonical Desktop V2 | `src/entries/resultApp.tsx` → `PortalPage` | `/result` (production) |
| Portal SPA | `src/entries/portalScreenshotApp.tsx` → `PortalApp` | `#/analyze`, `#/result` |

### 7.2 User Flow (legacy production)

```
/analyze (HTML form)
  → analyze.js: POST /backend/api/v1/analyze (BirthRequest)
  → BtePortal.ResultStore.save()
  → /result → resultApp.tsx → PortalPage
  → useCanonicalDesktopResult() → AnalyzeService.getCanonicalDesktopViewModel()
```

### 7.3 Interpretation Display

| UI | Component | Path |
|----|-----------|------|
| Canonical Desktop | `S08Interpretation` | `src/screens/canonical_desktop/sections/S08Interpretation.tsx` |
| Result V2 | `DomainSection` | `src/features/result_v2/components/DomainSection/` |
| Data source | `AnalysisDataDto.interpretation.sections[]` | API response |

### 7.4 Export Actions

| Action | Location | Implementation | Status |
|--------|----------|----------------|--------|
| In tư vấn (Print) | `CommercialRail.tsx` | `window.print()` + `reportMode="print"` | PARTIAL |
| Tải PDF | `CommercialRail.tsx` | Toast only — no binary PDF | STUB |
| Lưu báo cáo | `CommercialRail.tsx` | Local `saved` state | STUB |
| HTML/MD download | `reports.js` | Blob download from stored analyze result | IMPLEMENTED |
| PDF URL | `reports.js` | Opens URL if `https://...` in payload | NOT PROVIDED by API |
| DOCX | — | Not found | NOT IMPLEMENTED |

### 7.5 State Management

- React `useState` (`analysisSession` in PortalApp)
- `BtePortal.ResultStore` (localStorage: `bte_last_result`, `bte_history`)
- No Redux/Zustand
- `CanonicalReportInput` adapter exists at `src/features/result_v2/adapter/reportInput.ts` — **prepared but not wired to export**

---

## 8. Existing PDF Capability

**Assessment: PARTIAL**

### 8.1 Dependencies

| Library | In requirements.txt | Installed (audit env) | Production use |
|---------|--------------------|-----------------------|----------------|
| reportlab | **No** | **No** (ModuleNotFoundError) | Legacy `pdf_renderer.py`, IE renderer |
| simple_pdf (stdlib) | N/A (built-in) | Yes | **WP6 build_full, narrative formatter** |
| playwright | **No** | Unknown | QA only (`validation/portal_qa_audit.py`) |
| weasyprint, wkhtmltopdf, xhtml2pdf, pdfkit, pypdf, fpdf | **No** | No | Not found |

### 8.2 Implementations

| Implementation | Path | Classification |
|----------------|------|----------------|
| `write_simple_pdf()` | `engines/report_engine/simple_pdf.py` | IMPLEMENTED — Helvetica Latin-1, Vietnamese chars replaced |
| `PdfSerializer` | `engines/analysis_engine/report_generator/pdf_serializer.py` | IMPLEMENTED — uses simple_pdf_bytes |
| `PDFRenderer` (reportlab) | `engines/report_engine/pdf_renderer.py` | LEGACY — import fails without reportlab |
| `PdfRenderer` (RX-1) | `engines/report_engine/rendering/pdf_renderer.py` | STUB — returns JSON envelope, not PDF bytes |
| `PdfRenderer` (IE) | `engines/interpretation_engine/renderer/pdf_renderer.py` | LEGACY — reportlab |

### 8.3 Tests

- `tests/report_engine/test_pdf_renderer.py` — tests RX-1 stub renderer
- `tests/report_generator/test_unit_report_generator.py` — analysis_engine PDF serializer
- `tests/report_engine/` — **58 passed** (module scope)

### 8.4 HTML → PDF

**No HTML-to-PDF pipeline.** PDF is generated from flattened text lines, not from HTML/CSS.

### 8.5 Download Endpoint

**None.** Case export supports json/markdown/html only.

---

## 9. Existing DOCX Capability

**Assessment: NOT IMPLEMENTED (production)**

### 9.1 Dependencies

| Library | In requirements | Installed | Production use |
|---------|--------------|-----------|----------------|
| python-docx | **No** | **No** | Legacy WordRenderer only |

### 9.2 Implementations

| Implementation | Path | Classification |
|----------------|------|----------------|
| `WordRenderer` | `engines/report_engine/word_renderer.py` | LEGACY — import fails |
| `DocxRenderer` (RX-1) | `engines/report_engine/rendering/docx_renderer.py` | STUB — JSON envelope |
| `DocxRenderer` (IE) | `engines/interpretation_engine/renderer/docx_renderer.py` | LEGACY — python-docx |

### 9.3 Templates

No `.docx` template files found. No docxtpl.

### 9.4 Tests

- `tests/report_engine/test_docx_renderer.py` — tests RX-1 stub (JSON content, not real DOCX)

### 9.5 API Endpoint

**None.**

---

## 10. HTML Rendering Capability

**Assessment: PARTIAL**

### 10.1 Implementations

| Source | Path | Output quality |
|--------|------|----------------|
| Portal report view | `engines/report_engine/portal_view.py` | Basic `<h1>/<h2>/<p>` from sections — **production** |
| ReportFormatter | `engines/report_engine/formatter.py` | Structured ReportModel → HTML |
| HtmlRenderer (RX-1) | `engines/report_engine/rendering/html_renderer.py` | Identity blocks only (`data-block`, no content/CSS) |
| analysis_engine | `report_generator/html_serializer.py` | StructuredReport HTML |
| Jinja2 | — | **NOT IMPLEMENTED** |

### 10.2 Template Loader

- `KnowledgeTemplateLoader` — reads `engines/interpretation_engine/knowledge/06_report_templates/`
- `TemplateLoader` — local `templates/default.md` (legacy markdown)

### 10.3 Print CSS

| Location | Content |
|----------|---------|
| `applications/customer_portal/static/css/domain.css` | `@media print`, `.bte-exec-page-break` |
| `src/styles/components/business/four-pillars.css` | `@media print`, `page-break-inside: avoid` |
| `engines/analysis_engine/report_generator/theme.py` | `@media print`, `page-break` rules |
| `docs/reports/**/preview/*.html` | Print styles in design previews |

**No dedicated `report_v1.css` for export.**

### 10.4 Page-break Rules

Present in portal CSS and analysis_engine theme — usable for print-via-browser, not wired to server-side PDF.

---

## 11. Existing Templates and Assets

| Asset | Path | Binding | Classification |
|-------|------|---------|----------------|
| IE report templates (runtime) | `engines/interpretation_engine/knowledge/06_report_templates/` | `KnowledgeTemplateLoader` + `SectionBuilderRegistry` | **runtime-used** (WP6 path) |
| Knowledge report templates | `knowledge/report_templates/` | Not loaded by production orchestrator | documentation-only |
| Report presets package | `knowledge/packages/report_presets/` | Registry/manifest | unused in API path |
| Default MD template | `engines/report_engine/templates/default.md` | TemplateLoader (legacy) | legacy |
| UI preview HTML | `docs/reports/**/preview/` | Static design artifacts | documentation-only |
| Integration layer specs | `knowledge/10_integration_layer/01_REPORT_CONTRACT/` | Spec | documentation-only |
| Architecture pack 05 | `knowledge/architecture/pack_05_report_engine/` | Spec | documentation-only |
| `.specs/report_engine.md` | Root | Spec | documentation-only |

---

## 12. Golden Dataset Integration Point

### 12.1 Canonical Roots

| Root | Purpose |
|------|---------|
| `tests/golden_dataset/` | **Operational** — pytest, runner, validator, snapshots |
| `knowledge/golden_dataset/` | Framework docs only (no case JSON) |
| `knowledge/pilot/cases/CASE-0001/` | **Nguyễn Tiến Sơn** pilot case |

### 12.2 Existing case_0001

| File | Content |
|------|---------|
| `tests/golden_dataset/inputs/case_0001.json` | 1987-01-21T04:15+07, Hà Tây — **no subject name** |
| `tests/golden_dataset/expected/case_0001.json` | Minimal V1 `{success, sections, text}` |
| `tests/golden_dataset/snapshots/report_engine/case_0001.json` | Full report sections (tong_quan, tinh_cach, …) |
| `knowledge/pilot/cases/CASE-0001/input.json` | Nguyễn Tiến Sơn, 04:30, Hà Nội, confirmed pillars |

### 12.3 Recommendation for CASE_0001 (Nguyễn Tiến Sơn)

| Concern | Recommended location |
|---------|---------------------|
| Subject identity + pilot rules | `knowledge/pilot/cases/CASE-0001/` (keep) |
| Engine regression / report snapshot | `tests/golden_dataset/snapshots/report_engine/case_0001.json` (extend in WP-RPT-002+) |
| New Simple Report Export V1 expected | `tests/golden_dataset/expected/report_v1/case_0001.json` (proposed — CREATE in WP-RPT-002) |
| Input alignment | Update `tests/golden_dataset/inputs/case_0001.json` metadata to reference CASE-0001 (WP-RPT-002 decision) |

**Do not create CASE_0001 in WP-RPT-001** — documented only.

### 12.4 Schema Mismatch Issue

`input_schema.json` expects `birth.datetime`; fixtures use `birth.solar_datetime`. `golden_adapter.py` bridges at runtime.

---

## 13. Gaps

### Critical (blocks report generation)

1. **No unified ReportInputV1** — production uses thin portal dict, WP6 uses ReportModel, RX-1 uses separate upstream inputs.
2. **No API endpoint for PDF/DOCX binary download.**
3. **No real PDF/DOCX renderer** in RX-1 path (stubs only).
4. **simple_pdf cannot render Vietnamese** (Latin-1 replacement) — blocks production-quality PDF for BTE.
5. **reportlab / python-docx not in requirements** — legacy renderers fail import.

### High (report works but not production-ready)

1. Production `render_from_analysis` ignores chart, score, pattern — report is interpretation-only prose.
2. **Three parallel report subsystems** (portal_view, WP6 builder, analysis_engine/report_generator) — coupling risk.
3. Frontend PDF button is stub; no server-side export.
4. **Duplicate InterpretationResult models** — risk of wrong contract in WP-RPT-002.
5. CASE_0001 input divergence (04:15 vs 04:30, location, no name in test fixture).

### Medium (can defer)

1. Jinja2/HTML template system not present.
2. Public `/api/v1/analysis` port unbound.
3. `CanonicalReportInput` TS adapter not wired.
4. Golden dataset expected schema vs actual mismatch.

### Low (polish)

1. Template coverage reporting not exposed via API.
2. Narrative vs report distinction in UI export labels.
3. Playwright PDF (browser print) not productized.

---

## 14. Proposed Simple Report Export V1 Boundary

```
Existing BTE Pipeline (OrchestratorService)
        ↓
AnalysisResult (bazi + score + pattern + interpretation views)
        ↓
ReportInputV1 (new canonical contract — aggregate subject + chart + interpretation + metadata)
        ↓
Report Assembly (reuse WP6 builder OR RX-1 pipeline — pick ONE in WP-RPT-002)
        ↓
HTML Preview (portal-quality template + print CSS)
        ├── PDF (requires font-aware renderer — reportlab or weasyprint decision)
        └── DOCX (python-docx + template)
```

**Why not identical to current production path:** `render_from_analysis()` only mirrors interpretation sections to markdown/html. Simple Report Export V1 needs subject header, chart summary, branded layout, and binary export — requiring `ReportInputV1` and a single assembly path.

**Recommended primary reuse:** WP6 `ReportBuilder` + `portal_view` HTML patterns + RX-1 `ExportManager` plugin architecture (replace stub renderers with real binary producers).

---

## 15. Recommended WP-RPT-002 Scope

### CREATE

| File / artifact | Purpose |
|-----------------|---------|
| `engines/report_engine/contracts/report_input_v1.py` | ReportInputV1 dataclass |
| `engines/report_engine/export/html_exporter.py` | Branded HTML from ReportInputV1 |
| `engines/report_engine/export/pdf_exporter.py` | Real PDF (font-aware) |
| `engines/report_engine/export/docx_exporter.py` | Real DOCX |
| `engines/report_engine/templates/report_v1.html` | HTML template |
| `engines/report_engine/templates/report_v1.css` | Print CSS |
| `applications/api/routes/export.py` or extend v1 | `GET/POST .../report/export?format=pdf|docx|html` |
| `tests/report_engine/test_report_export_v1.py` | Export module tests |
| `tests/golden_dataset/expected/report_v1/case_0001.json` | Expected export metadata (not binary) |

### MODIFY

| File | Change |
|------|--------|
| `applications/api/services/orchestrator.py` | Optional: build ReportInputV1 at report stage |
| `engines/report_engine/engine.py` | Add `export_v1()` wrapper (backward compatible) |
| `engines/report_engine/rendering/pdf_renderer.py` | Replace stub with real PDF OR delegate to pdf_exporter |
| `engines/report_engine/rendering/docx_renderer.py` | Replace stub with real DOCX |
| `requirements.txt` or `applications/requirements.txt` | Add reportlab and/or python-docx (explicit decision) |
| `applications/customer_portal/src/features/portal/components/CommercialRail.tsx` | Wire PDF/DOCX to API |
| `applications/customer_portal/static/js/reports.js` | Call export endpoint |

### REUSE

| Component | Path |
|-----------|------|
| OrchestratorService | `applications/api/services/orchestrator.py` |
| InterpretationResult (runtime) | `engines/interpretation_engine/legacy_builder.py` |
| portal_view HTML patterns | `engines/report_engine/portal_view.py` |
| ReportBuilder / KnowledgeTemplateLoader | `engines/report_engine/builder.py` |
| CanonicalReportPipeline | `engines/report_engine/pipeline/` |
| ExportManager plugin pattern | `engines/report_engine/rendering/export_manager.py` |
| Golden dataset harness | `tests/golden_dataset/` |
| Portal print CSS | `static/css/domain.css` |
| Pilot CASE-0001 | `knowledge/pilot/cases/CASE-0001/` |

### DO NOT TOUCH

| Area | Reason |
|------|--------|
| Foundation / Design System packs | Frozen per foundation_v1 rules |
| Golden Dataset snapshots (existing) | Rule: no modify without explicit request |
| Interpretation Engine rule logic | Out of scope |
| Calendar / Bazi / Score engines | Module boundary |
| `knowledge/golden_dataset/` framework docs | Docs-only |
| Public API renames | Backward compatibility |

---

## 16. Risks

| Risk | Severity | Evidence |
|------|----------|----------|
| Duplicate InterpretationResult models | High | 4+ classes across codebase |
| Legacy vs RX-1 vs WP6 pipeline divergence | High | Different entry points, different outputs |
| Spec vs implementation mismatch | High | `knowledge/architecture/pack_05_report_engine/` vs production portal_view |
| Frontend/backend contract mismatch | Medium | Portal expects PDF URL; API never provides |
| reportlab/python-docx not pinned | High | Import fails in clean env |
| Windows/Linux render differences | Medium | Font paths, weasyprint deps |
| Vietnamese font in PDF | Critical | simple_pdf Latin-1 strips diacritics |
| Timezone/calendar data loss | Medium | BirthRequest uses int fields; golden uses ISO datetime + lat/long |
| Hidden coupling to legacy_builder | Medium | All truth adapters import legacy InterpretationResult |
| Triple orchestrator run in POST /analysis | Medium | Performance, inconsistent if stages cached differently |

---

## 17. Final Recommendation

### Status: **READY WITH BLOCKERS**

### Blockers to resolve before / at start of WP-RPT-002

1. **Choose single report assembly path** (WP6 builder vs RX-1 pipeline vs new thin layer).
2. **Define ReportInputV1 contract** explicitly (fields from AnalysisResult + subject metadata).
3. **Select PDF technology** (reportlab with Vietnamese font vs weasyprint HTML→PDF) and add to requirements.
4. **Add python-docx** to requirements if DOCX in V1 scope.
5. **Align CASE_0001 birth input** (04:30 Hà Nội vs 04:15 Hà Tây) before golden validation.

### Proceed when

- WP-RPT-002 design review approves boundary in §14.
- Font strategy for Vietnamese PDF is decided.
- API export endpoint shape is agreed.

---

## Appendix A — CASE_0001 Input Requirements Audit

### Subject (reference only — not in production code)

```
Nguyễn Tiến Sơn / Nam / 21/01/1987 / giờ Dần (~04:00) / Việt Nam
```

### API BirthRequest (Portal / POST /api/v1/analyze)

| Field | Format | Required | Notes |
|-------|--------|----------|-------|
| year, month, day | int | Yes | Portal wizard validates ranges |
| hour, minute | int (0–23, 0–59) | Yes (default 0) | Giờ Dần ≈ 03:00–04:59 → use hour=4, minute=30 (pilot) or 15 (test fixture) |
| gender | string ("male"/"female") | Optional | Required for BaZi |
| timezone | string | Default `Asia/Ho_Chi_Minh` | |
| full_name | string | Optional | Presentation only — **not passed to engines** |
| birth_place | string | Optional | Presentation only |
| latitude/longitude | — | **Not in BirthRequest** | Golden dataset has them; API does not |

### Golden Dataset Input (tests/golden_dataset)

| Field | Format |
|-------|--------|
| birth.solar_datetime | ISO 8601 with offset |
| birth.timezone | IANA |
| birth.location | country, province, district, lat, long |
| options.calendar | calendar_type, use_true_solar_time, use_dst |
| options.engine | language, rule_database, output_format |

### Issues for exact reproduction

| Issue | Severity |
|-------|----------|
| API lacks lat/long → true solar time may differ | Medium |
| Pilot 04:30 vs test 04:15 → different hour pillar edge case | High for CASE_0001 |
| Giờ Dần ambiguous without exact minute | Medium |
| Subject name not in engine input | Low (report header only) |

---

## Appendix B — Validation Commands Executed

```bash
git status --short          # clean (no output)
git branch --show-current   # release/v1.0-final
python -m pytest tests/report_engine -q   # 58 passed in 0.64s
python -c "import reportlab"              # ModuleNotFoundError
python -c "import docx"                   # ModuleNotFoundError
```

No production files modified. Only this audit document created.

---

## Appendix C — Git Status (post-audit)

```
Branch: release/v1.0-final
Untracked/new: knowledge/report_v1_validation/WP_RPT_001_CURRENT_STATE_AUDIT.md
No modified tracked files
```

---

*End of WP-RPT-001 audit. Do not proceed to WP-RPT-002 without review.*
