# PACK 06 — DATE SELECTION REPORT ENGINE

# FINAL FREEZE REPORT

**Sprint:** P6-06 FINAL FREEZE  
**Date:** 2026-08-28  
**Sample:** Nguyễn Tiến Sơn · Nam · 21/01/1987 · tháng 09/2026  
**Decision:** PASS

```text
PACK 06
DATE SELECTION REPORT ENGINE
FINAL FREEZE
PASS
```

This sprint was verification only. No features, UI redesign, algorithm changes, report changes, PDF changes, DOCX changes, or API redesign were introduced.

---

## Executive Summary

PACK 06 is the reporting layer for **Chọn ngày tốt**. Date Selection computes a result once. The adapter copies that snapshot into an immutable `DateSelectionReportModel`. PDF and DOCX render from the same model. The Customer Portal exports the currently displayed search result without recalculation.

P6-06 re-ran architecture review, module tests, live PDF/DOCX generation, Microsoft Word open, and a real `/choose-date` search → Top-5 → PDF/DOCX download.

Every mandatory acceptance item passed.

---

## Completed Architecture

The architecture set under `knowledge/pack_06_date_selection_report_engine/` was not modified during implementation or this freeze. Documents remain the canonical specification:

| Document | Role |
|----------|------|
| `PACK_06_DATE_SELECTION_REPORT_ENGINE_ARCHITECTURE.md` | Architecture |
| `01_DATA_MODEL.md` | Data Model |
| `02_RUNTIME_PIPELINE.md` | Runtime Pipeline |
| `03_PUBLIC_API.md` | Public API |
| `04_REPORT_LAYOUT.md` | Report Layout |
| `05_RENDER_ENGINE.md` | Render Engine |
| `06_EXPORT_ENGINE.md` | Export Engine |
| `07_TEMPLATE_ENGINE.md` | Template Engine |
| `08_VALIDATION.md` | Validation |
| `09_TESTING.md` | Testing |
| `10_ACCEPTANCE.md` | Acceptance |

Canonical flow (unchanged):

```text
Date Selection Engine
        ↓
Canonical Search Result
        ↓
DateSelectionReportAdapter
        ↓
DateSelectionReportModel
        ↓
Report Composition / RenderTree
        ↓
PDF / DOCX
```

Business rule remains frozen: PACK 06 does not recalculate dates, hours, Cung Phi, Nạp Âm, Hạ Nguyên, Trạch, or khắc.

Architecture documents still carry the original header **DRAFT → CANONICAL REVIEW**. That is the frozen specification text. This report is the implementation and acceptance freeze; the architecture files were not rewritten.

---

## Completed Implementation

Implemented sprints, mapped to the frozen pipeline:

| Sprint | Deliverable |
|--------|-------------|
| P6-01 | `DateSelectionReportModel`, adapter, integrity validation |
| P6-02 | Render context, tokens, labels, `DateSelectionRenderTree`, template package |
| P6-03 / P6-03A/B | Playwright PDF, commercial print CSS — PDF FROZEN |
| P6-04 | python-docx named styles, eastAsia Unicode — DOCX FROZEN |
| P6-05 / P6-05A | Portal `/choose-date` export + live API `POST /report/pdf` and `/report/docx` |
| P6-06 | This acceptance review |

Foundation freeze confirmed in code:

- `DateSelectionReportModel` is `@dataclass(frozen=True, slots=True)`.
- `DateSelectionReportAdapter.adapt()` consumes `SearchResult.to_dict()` only. It does not call `DateSelectionService.search`.
- Validators check completeness and allowed labels. They do not score or rerank.
- API export uses `DisplayedSearchResult` (the portal snapshot). Tests monkeypatch `search()` to prove export does not rerun Date Selection.

Public export routes on the live API (verified 200 OpenAPI):

- `POST /api/v1/date-selection/search`
- `POST /api/v1/date-selection/report/pdf`
- `POST /api/v1/date-selection/report/docx`

---

## Completed Tests

Module tests only (no full-project pytest):

```text
python -m pytest tests/date_selection_report applications/api/tests/test_date_selection.py applications/api/tests/test_date_selection_report_export.py applications/customer_portal/tests/test_date_selection_pages.py applications/customer_portal/tests/test_date_selection_export_proxy.py -q
→ 65 passed

npx vitest run tests/js/date_selection.test.tsx
→ 32 passed
```

Coverage includes models, adapter, validation, render tree, template validation, PDF, visual polish, DOCX, API export without recalculation, portal pages, and portal `/backend` proxy.

No tests, snapshots, golden datasets, or expected outputs were changed in this sprint.

---

## Completed Manual Verification

Sample case: **Nguyễn Tiến Sơn / Nam / 21/01/1987 / 09/2026**.

Evidence:

- `artifacts/pack_06_p6_06/bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.pdf` (199 407 bytes, 7 pages)
- `artifacts/pack_06_p6_06/bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.docx` (37 736 bytes)
- `artifacts/pack_06_p6_06/screenshots/pdf_page_01.png` … `pdf_page_07.png`
- `artifacts/pack_06_p6_06/browser/` live portal downloads
- `artifacts/pack_06_p6_06/freeze_verify.json`

### PDF (opened, 7 pages)

| Check | Result |
|-------|--------|
| Header | PASS — BÁO CÁO CHỌN NGÀY TỐT / BTE PLATFORM / 28/08/2026 |
| Executive Summary | PASS — Khách hàng, Nhóm Trạch, 09/2026, 5 ngày đề xuất |
| Person | PASS — THÔNG TIN NGƯỜI XEM |
| Search | PASS — THÔNG TIN TÌM NGÀY TỐT |
| Recommendation | PASS — CÁC NGÀY ĐỀ XUẤT, ranks 01–05 |
| Compatible Hours | PASS — Giờ phù hợp Nhóm Trạch của bạn |
| Positive Times | PASS — Đại An / Tốc Hỷ / Tiểu Cát |
| Guidance | PASS — HƯỚNG DẪN THAM KHẢO (page 7) |
| Footer | PASS — Generated by BTE Platform · page · 1.0; body footer BTE Platform · Báo cáo chọn ngày tốt · 1.0 |
| Unicode | PASS — Nguyễn Tiến Sơn and diacritics render |
| Page order | PASS — cover → recommendations 01–05 → guidance |
| Recommendation order | PASS — 04/09/2026, 24/09/2026, 06/09/2026, 10/09/2026, 14/09/2026 |

### DOCX (opened in Microsoft Word)

| Check | Result |
|-------|--------|
| Editable | PASS — Word `ReadOnly=false`, `ProtectionType=-1` (unprotected), 317 paragraphs |
| Unicode | PASS — `Nguyễn Tiến Sơn` in document.xml; eastAsia font hint on named styles |
| Styles | PASS — ReportTitle, SectionTitle, RecommendationTitle, Result, Label, Value, Caption, Footer |
| Recommendation order | PASS — same five solar dates, same order as SearchResult |
| Compatible Hours | PASS |
| Positive Times | PASS |

### Portal

Live `http://127.0.0.1:8081/choose-date`:

Search → 5 ranked cards → **Tải PDF** → **Tải DOCX**.

Downloads succeeded (`%PDF-` / `PK`). Files open with the same sections and recommendation order. No page errors. No customer-facing export error.

---

## Regression

PACK 06 commits did not modify Calendar, Date Selection Engine, Ranking, Ganzhi, Hạ Nguyên, Bazi, Interpretation, or PACK 05 Report Engine sources.

Customer Portal received Date Selection export actions only (P6-05). Result-page / PACK 05 export paths were not redesigned.

| Area | Status |
|------|--------|
| Calendar | unchanged |
| Date Selection Engine | unchanged |
| Ranking | unchanged |
| Ganzhi | unchanged |
| Hạ Nguyên | unchanged |
| PACK 05 | unchanged |
| Customer Portal (core / Result) | unchanged except Date Selection export glue |
| Bazi | unchanged |
| Interpretation | unchanged |

---

## Commercial Quality

The PDF is a consulting report: navy hierarchy, Vietnamese labels, Trach-matched hours, grouped positive times, educational guidance without promises. The DOCX is the same content in editable named styles, suitable for a consultant to annotate in Word.

Suitable for consultant delivery: **yes**.

---

## Final Checklist

| Item | Result |
|------|--------|
| Architecture | PASS |
| Data Model | PASS |
| Pipeline | PASS |
| API | PASS |
| Template | PASS |
| Render | PASS |
| Export | PASS |
| Validation | PASS |
| Testing | PASS |
| PDF | PASS |
| DOCX | PASS |
| Portal Export | PASS |
| Regression | PASS |
| Commercial Quality | PASS |

---

## Known Limitations

These are frozen characteristics, not freeze blockers:

1. Architecture documents keep original phase IDs (P6-03 Layout, P6-04 PDF, …). Implemented sprint names used PDF then DOCX then Portal. The documents were left unchanged by design.
2. Chromium print chrome uses the English line `Generated by BTE Platform`. The report body footer is Vietnamese. This is the frozen P6-03 PDF chrome.
3. Cover page (page 1) does not fill the full A4 height after Person and Search. Later recommendation pages are dense. Accepted in P6-03 visual freeze.
4. Empty-recommendation export remains dormant: P6-01 validation requires at least one ranked date.
5. Export requires the displayed `SearchResult` snapshot. It will not reconstruct a report from DOM or from a new search.

---

## Release Decision

All mandatory items passed.

```text
PACK 06
DATE SELECTION REPORT ENGINE
FINAL FREEZE
PASS
```

PACK 06 is production-ready for consultant delivery of Date Selection PDF and DOCX reports from the Customer Portal.
