# WP-RPT-002 — ReportInputV1 + CASE-0001 + HTML Preview Foundation

**Status:** COMPLETE  
**Date:** 2026-08-12  
**Branch:** `release/v1.0-final`

---

## 1. Summary

WP-RPT-002 delivers the **ReportInputV1** contract, runtime adapter, WP6 compatibility bridge, CASE-0001 canonicalization, golden snapshot, and **HTML Report V1** renderer.

No PDF, DOCX, Portal, or API export changes were made.

---

## 2. ReportInputV1 Contract

| Item | Value |
|------|-------|
| Path | `engines/report_engine/contracts/report_input_v1.py` |
| Main symbol | `ReportInputV1` |
| Version constant | `REPORT_INPUT_VERSION = "1.0"` |
| Serialization | `ReportInputV1.to_dict()` (deterministic, sorted keys) |

### Sections

```
ReportInputV1
├── metadata
├── profile
├── calendar
├── pillars
├── five_elements
├── strength
├── ten_gods
├── pattern
├── useful_god
├── shensha
├── luck_cycles
├── interpretation
└── diagnostics
```

---

## 3. Adapter

| Item | Value |
|------|-------|
| Path | `engines/report_engine/adapters/report_input_v1_adapter.py` |
| Main symbols | `ReportInputV1Adapter`, `ReportInputV1Source`, `build_report_input_v1()` |

### Input sources (priority)

1. `AnalysisResult` (views: bazi, strength, pattern, useful_god, score, interpretation)
2. `InterpretationResult` (legacy canonical — when analysis view absent)
3. `calendar` / `luck` dict payloads from orchestrator shaping
4. Explicit `ReportProfileV1` metadata
5. Optional fields → `None` + `diagnostics.missing_fields`

### Fallback behavior

- Missing slices recorded in `diagnostics.missing_fields`
- No invented professional content
- Legacy `InterpretationResult` read via safe payload helper (avoids `mappingproxy` deepcopy failure on `luck_context`)

---

## 4. CASE-0001 Canonicalization

### Canonical input

| Field | Value |
|-------|-------|
| Case ID | `CASE-0001` |
| Name | Nguyễn Tiến Sơn |
| Gender | male |
| Birth | 1987-01-21 04:30 |
| Timezone | Asia/Bangkok |
| Birth place | Hà Tây, Việt Nam |
| Pillars | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |

### Golden dataset path

```
tests/golden_dataset/report_v1/CASE-0001/
├── input.json
├── expected_report_input.json
└── README.md
```

### Conflicts resolved

| Source | Status |
|--------|--------|
| `tests/golden_dataset/report_v1/CASE-0001/` | **CANONICAL for Report V1** |
| `knowledge/pilot/cases/CASE-0001/` | Pilot reference (location: Hà Nội) — not overwritten |
| `tests/golden_dataset/inputs/case_0001.json` | **LEGACY** (04:15, different schema) — not overwritten |

---

## 5. WP6 Integration

| Component | Path | Role |
|-----------|------|------|
| Compatibility bridge | `engines/report_engine/adapters/wp6_assembly_bridge.py` | `ReportInputV1` → interpretation dict |
| WP6 builder | `engines/report_engine/service.py` | `ReportService.build()` |
| Section templates | `KnowledgeTemplateLoader` + `06_report_templates` | Unchanged |

### API

```python
from engines.report_engine.adapters import build_report_model_from_input

model = build_report_model_from_input(report_input)
```

---

## 6. HTML Preview V1

| Item | Value |
|------|-------|
| Renderer | `engines/report_engine/rendering/html_report_v1.py` |
| Class / API | `HtmlReportV1Renderer.render()` / `render_html()` |
| Template | `engines/report_engine/templates/v1/report_v1.html` |
| CSS | `engines/report_engine/templates/v1/report_v1.css` |

### Sections rendered (18)

Header, chart info, four pillars, five elements, strength, ten gods, pattern, useful god, shen sha, luck cycles, executive summary, career, wealth, marriage, health, children, recommendations, conclusion.

Missing data → neutral fallback: *"Chưa đủ dữ liệu để đưa ra kết luận."*

### Local preview

```
knowledge/report_v1_validation/previews/CASE-0001.html
```

Regenerate via command in `tests/golden_dataset/report_v1/CASE-0001/README.md`.

---

## 7. Known Missing / Thin Runtime Data (CASE-0001)

| Field | Status |
|-------|--------|
| `five_elements` raw breakdown | Empty — score wuxing_series not populated for this case |
| `calendar.calendar_mode` | Missing — recorded in diagnostics |
| `luck_cycles.direction` / `start_age` | Partial — only `current_dayun` available |
| `interpretation.executive_summary` | Empty — content lives in section bodies |
| Domain sections (wealth, children) | Fallback text when no matching section |

---

## 8. Tests

| Suite | Result |
|-------|--------|
| `tests/report_engine` (baseline) | 58 passed (pre-WP-RPT-002) |
| New tests | +15 |
| **Total** | **73 passed** |
| Failures | 0 |

### New test files

- `tests/report_engine/test_report_input_v1.py`
- `tests/report_engine/test_report_input_v1_adapter.py`
- `tests/report_engine/test_html_report_v1.py`
- `tests/report_engine/test_case_0001_report_input.py`
- `tests/report_engine/case_0001_runtime.py`

---

## 9. Recommended WP-RPT-003 Boundary

1. PDF export using HTML + print CSS (`report_v1.css` foundation)
2. Font strategy for Vietnamese PDF (embedded Noto or system stack decision)
3. API export endpoint (`/report/export?format=pdf`)
4. Portal wire-up for preview/download
5. Stabilize `five_elements` mapping when score series available
6. Optional: enrich `luck_cycles` from luck metadata when dayun list exposed

**Do not start WP-RPT-003 without review of `CASE-0001.html` preview.**

---

## 10. Related Documents

- WP-RPT-001 audit: `knowledge/report_v1_validation/WP_RPT_001_CURRENT_STATE_AUDIT.md`
- CASE-0001 README: `tests/golden_dataset/report_v1/CASE-0001/README.md`
