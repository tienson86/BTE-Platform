# WP-RPT-003 — PDF + DOCX Export V1

**Status:** COMPLETE  
**Date:** 2026-08-12  
**Branch:** `release/v1.0-final`

---

## 1. Summary

WP-RPT-003 adds **production PDF and DOCX export** for Report V1, built on the WP-RPT-002 foundation (`ReportInputV1` → HTML Report V1).

No Portal, HTTP API, or engine logic changes were made.

### Target flow

```text
ReportInputV1
      ↓
ReportExportServiceV1
      ├── HtmlReportV1Renderer → PdfExporterV1 (Playwright)
      └── DocxExporterV1 (python-docx)
```

---

## 2. Architecture

| Component | Path | Symbol |
|-----------|------|--------|
| Export result contract | `engines/report_engine/contracts/report_export_result_v1.py` | `ReportExportResultV1` |
| Filename helpers | `engines/report_engine/exporting/filename.py` | `build_export_filename()` |
| PDF exporter | `engines/report_engine/exporting/pdf_exporter_v1.py` | `PdfExporterV1` |
| DOCX exporter | `engines/report_engine/exporting/docx_exporter_v1.py` | `DocxExporterV1` |
| Export service | `engines/report_engine/services/report_export_service_v1.py` | `ReportExportServiceV1` |

Exporters consume **only** `ReportInputV1`. They do not call Calendar, BaZi, Analysis, Interpretation, or Orchestrator.

PDF reuses:

- `HtmlReportV1Renderer`
- `engines/report_engine/templates/v1/report_v1.html`
- `engines/report_engine/templates/v1/report_v1.css`

Goal: **HTML preview and PDF share the same visual source.**

---

## 3. PDF renderer choice

### Evaluated options

| Library | Result |
|---------|--------|
| **WeasyPrint** | Installed but **not viable on Windows dev** without GTK/Pango (`libgobject-2.0-0` missing). Suitable for Linux with system packages. |
| **Playwright / Chromium** | **Selected** — works on Windows, supports UTF-8 HTML, CSS print, A4, tables, page breaks. |

### Why Playwright

- Single Python dependency (`playwright`) plus Chromium browser binary.
- Renders the same HTML/CSS as the preview — no second PDF layout.
- Full Vietnamese Unicode via browser font stack.
- Stable print-to-PDF API.

### Not used

- `simple_pdf.py` (legacy Latin-1) — **not** used for Report V1 production.

---

## 4. Dependencies

Added to `requirements-dev.txt`:

```text
playwright>=1.49.0
python-docx>=1.1.2
```

### Post-install (required once per environment)

```bash
pip install -r requirements-dev.txt
playwright install chromium
```

### Import smoke

```bash
python -c "from playwright.sync_api import sync_playwright; import docx"
```

---

## 5. Font strategy (PDF)

PDF inherits HTML/CSS font stack from `report_v1.css`:

```text
Arial, "Segoe UI", "Noto Sans", "DejaVu Sans", sans-serif
```

- Content preserves Vietnamese diacritics (e.g. Nguyễn Tiến Sơn, Bính Dần).
- Filenames strip diacritics for cross-platform safety (`ascii_slug()`).
- No font binaries committed to the repository.

---

## 6. DOCX strategy

- Library: **python-docx** (OpenXML `.docx`, editable in Microsoft Word).
- Structure mirrors HTML V1 sections (01–17+).
- Tables used for profile, Tứ Trụ, Ngũ hành, Đại vận where structured data exists.
- Styles: Title, Heading 1, Heading 2, Normal, Table Text.
- A4 page size with reasonable margins.
- **Editability > pixel-perfect fidelity** vs PDF.

Missing section data uses the WP-RPT-002 fallback:

```text
Chưa đủ dữ liệu để đưa ra kết luận.
```

---

## 7. Export Service API

```python
from engines.report_engine.services.report_export_service_v1 import ReportExportServiceV1

service = ReportExportServiceV1(export_root=Path("output/dir"))
pdf_result = service.export_pdf(report_input)   # optional output_path
docx_result = service.export_docx(report_input)
```

### `ReportExportResultV1` fields

| Field | Description |
|-------|-------------|
| `format` | `pdf` or `docx` |
| `file_path` | Absolute/resolved path string |
| `file_name` | Deterministic filename |
| `media_type` | `application/pdf` or DOCX OpenXML MIME |
| `size_bytes` | File size |
| `report_version` | From `ReportInputV1.metadata` |
| `case_id` | From `ReportInputV1.metadata` |
| `generated_at` | ISO UTC timestamp |
| `page_count` | PDF only, when estimable |

### Filename pattern

```text
BTE_{case_id}_{ascii_name}_Report_V{version}.{ext}
```

Example:

```text
BTE_CASE-0001_Nguyen_Tien_Son_Report_V1_0.pdf
```

(`1.0` → `V1_0` in filename.)

### PDF metadata

- **Title:** `Báo cáo luận giải Bát Tự — {profile.full_name}`
- **Author:** BTE Platform (via HTML `<title>` / document context)

---

## 8. CASE-0001 artifacts

Generated via canonical fixture → adapter → export service:

| Artifact | Path |
|----------|------|
| PDF | `knowledge/report_v1_validation/exports/BTE_CASE-0001_Nguyen_Tien_Son_Report_V1_0.pdf` |
| DOCX | `knowledge/report_v1_validation/exports/BTE_CASE-0001_Nguyen_Tien_Son_Report_V1_0.docx` |

Source: `tests/golden_dataset/report_v1/CASE-0001/` + `tests/report_engine/case_0001_runtime.py`

---

## 9. Tests

```bash
python -m pytest tests/report_engine -q
```

### New test modules

| File | Coverage |
|------|----------|
| `test_export_filename.py` | Deterministic naming, ASCII slug |
| `test_pdf_exporter_v1.py` | PDF creation, `%PDF`, validation, Playwright import |
| `test_docx_exporter_v1.py` | DOCX OpenXML, headings, Vietnamese |
| `test_report_export_service_v1.py` | Routing, MIME, metadata |
| `test_case_0001_exports.py` | Full integration + artifact generation |

### Vietnamese smoke strings

- Nguyễn Tiến Sơn
- Bát Tự
- Thân vượng nhược
- Dụng thần / Hỷ thần / Kỵ thần

DOCX: verified by text extraction.  
PDF: HTML source verified before render; file signature and size validated.

---

## 10. Deployment requirements

### Windows (development)

- `pip install playwright python-docx`
- `playwright install chromium` (downloads Chromium ~150MB)
- Works out of the box after browser install; no GTK/Pango needed.

### Linux (production)

- Same Python packages.
- Run `playwright install chromium` (or `playwright install-deps` for system libraries).
- Chromium runs headless; ensure sufficient memory for PDF generation.
- Alternative future path: WeasyPrint on Linux if ops prefers fewer browser dependencies (not selected for V1).

---

## 11. Known limitations

- PDF page-count estimation is best-effort (`/Count` scan), not a full PDF parser.
- DOCX layout is semantic, not pixel-matched to PDF.
- `executive_summary`, full `five_elements`, wealth/children slices may still show diagnostics gaps from upstream data — exporters do not invent content.
- Playwright adds Chromium as a runtime dependency; CI must install browser binaries.
- No HTTP download API or Portal buttons (WP-RPT-004).

---

## 12. Recommended WP-RPT-004

1. FastAPI endpoints: `/api/report/v1/pdf`, `/api/report/v1/docx`
2. Portal preview + download buttons wired to `ReportExportServiceV1`
3. Configurable `export_root` via application settings
4. Optional streaming response + customer storage integration
5. CI job: `playwright install chromium` before report export tests

---

## 13. REPORT DATA GAP (unchanged from WP-RPT-002)

Exporters surface existing `ReportInputV1` content only. Known upstream gaps (not fixed in WP-RPT-003):

- `five_elements` partial / missing in some runtime paths
- Full luck cycle tables
- Wealth, children, executive summary sections when interpretation slice absent

Recorded in `diagnostics.missing_fields`; no engine changes made.
