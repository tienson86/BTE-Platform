# WP-RPT-003A — CASE-0001 Report Content Normalization & Runtime Gap Closure

**Status:** COMPLETE  
**Date:** 2026-08-12  
**Branch:** `release/v1.0-final`

---

## 1. Summary

WP-RPT-003A normalizes **customer-facing report text** for CASE-0001 without changing architecture, engines, Rule Database, Portal, or API.

`ReportInputV1` remains the SSOT and is **unchanged** (golden snapshot still matches). HTML, PDF, and DOCX all render through one presentation + localization layer.

---

## 2. Architecture (unchanged pipeline)

```text
ReportInputV1
      ↓
build_presented_report()     ← localization + object unwrap + sentence filter
      ├── HtmlReportV1Renderer → PDF (Playwright)
      └── DocxExporterV1
```

Single mapping location:

```text
engines/report_engine/localization/
```

Renderers do not translate independently.

---

## 3. ISSUE-001 / 003 — Localization

Tables in `localization/labels_vi.py`:

| Domain | Example |
|--------|---------|
| gender | male → Nam |
| strength | strong → Thân vượng |
| pattern status | success → Đắc cách |
| temperature | hot → Nhiệt |
| season | winter → Đông |
| luck direction | forward → Thuận |
| confidence level | high → Cao |
| category | shensha → Thần sát |

API: `display_text(value, domain)`.

---

## 4. ISSUE-002 — Object leakage

`unwrap_display_object()` handles dict / dataclass / enum / Python repr.

CASE-0001 Tiết khí:

```text
{'name': 'Đại Hàn', 'index': 23}  →  Đại Hàn
```

Contract field still stores the repr string (snapshot preserved).

---

## 5. ISSUE-005 — Report-friendly interpretation

`customer_paragraphs()` drops instructional Rule Engine sentences (Áp dụng / Ưu tiên / Nếu / Kiểm tra / Kích hoạt / …).

Kept library conclusions only. No AI rewrite.

---

## 6. ISSUE-004 / 008 / 009 / 010 — Gaps

See `runtime_gap_report.md`.

Customer copy for named missing slices:

```text
DATA NOT PROVIDED BY RUNTIME
```

Executive summary empty after filter:

```text
Chưa có dữ liệu tổng hợp.
```

Five elements and full luck cycles are **not recalculated**. Adapter mapping misses are documented for a later WP.

---

## 7. ISSUE-006 — ShenSha audit

`audit_shensha_duplicates()` marks alias candidates. Names are not merged.

---

## 8. ISSUE-007 — Semantic equality

Shared model: `engines/report_engine/rendering/report_sections_v1.py`.

PDF reuses HTML. DOCX consumes the same sections (tables instead of pillar cards; same fields).

---

## 9. Tests

```bash
python -m pytest tests/report_engine -q
```

| Suite | Result |
|-------|--------|
| Baseline WP-RPT-002 (73) | PASS |
| WP-RPT-003 (19) | PASS |
| WP-RPT-003A new | 6 PASS |
| Total | **98 passed**, 0 failed |

Golden snapshot `expected_report_input.json` was not modified.

---

## 10. CASE-0001 artifacts

Regenerated after normalization. WP-RPT-003 copies kept under `wp_rpt_003_baseline/`.

See `case_0001_before_after.md`.

---

## 11. Files created

- `engines/report_engine/localization/` (labels, display, customer_text, shensha_audit)
- `engines/report_engine/rendering/report_sections_v1.py`
- `tests/report_engine/test_localization_v1.py`
- `knowledge/report_v1_validation/WP_RPT_003A_RUNTIME_NORMALIZATION.md`
- `knowledge/report_v1_validation/runtime_gap_report.md`
- `knowledge/report_v1_validation/case_0001_before_after.md`
- `knowledge/report_v1_validation/wp_rpt_003_baseline/`

## 12. Files modified

- `engines/report_engine/rendering/html_report_v1.py`
- `engines/report_engine/exporting/docx_exporter_v1.py`
- CASE-0001 HTML preview + PDF/DOCX exports (regenerated)

## 13. Not modified

Calendar, BaZi, Strength, Pattern, Useful God, ShenSha rules, Luck algorithm, Rule Database, Portal, API, golden dataset.

---

## 14. Recommended WP-RPT-003B

1. Adapter mapping for `wuxing_series` `label`/`value` → five elements (snapshot update authorized).
2. Adapter mapping for `current_dayun.metadata.sequence` → full luck cycles.
3. Interpretation Engine: commercial executive summary + wealth + children sentences.
4. Rule Database: ShenSha alias policy (Thiên Ất vs Thiên Ất Quý Nhân, …).
5. Then review CASE-0001 again before opening case #2.

**STOP** — no API, no Portal, no UI.
