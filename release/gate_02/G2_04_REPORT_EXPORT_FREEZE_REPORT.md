# G2-04 — Report / PDF / DOCX freeze report

**Status: G2-04: REPORT / PDF / DOCX FROZEN — READY FOR G2-05**

Date: 2026-08-21  
Entry: G2-03 narrative frozen  
Invariant: one analysis → one presentation model → Result / Full Report / HTML / PDF / DOCX

## Hard freeze

Gate-1 analytical engines and rules were not changed. G2-01R identity/routing, G2-02 Result semantics, and G2-03 narrative source stay frozen.

Official customer files are built from the **stored Analyze payload** (the same blob ResultStore shows). They do **not** re-run Calendar / BaZi / Strength / Pattern / Useful God.

If an export had differed because canonical analysis differed, this gate would have **stopped**. Ten control cases: **0 analytical diffs**.

## Canonical presentation model

```
Stored AnalysisResult JSON (UsefulGodView@1.5 + pack05_narrative_result_v1)
  → applications.api.services.customer_report_input.build_customer_report_input
  → ReportInputV1
  → engines.report_engine.rendering.report_sections_v1.build_presented_report
  → PresentedReportV1
  → HTML Report V1 / Playwright PDF / python-docx
```

Renderers may paginate and style differently. They must not derive Dụng, Hỷ, Strength, Pattern, or Luck on their own.

## Official PDF vs Print

| Path | Customer label | Authority |
|------|----------------|-----------|
| `POST /api/v1/export/pdf` | **Tải PDF** | **OFFICIAL PDF** — Report V1 HTML printed by Playwright Chromium |
| Browser `window.print()` on `/result` | **In** | **PRINT VIEW** — convenience print of Result UI. Not a second report product |
| `/reports` HTML preview | **Xem báo cáo** | On-screen Full Report from the same stored payload |

There is no second button named “Xuất PDF”. Sidebar “Xuất báo cáo” scrolls to the export bar; it does not print.

## Customer DOCX

`POST /api/v1/export/docx` wires the existing `DocxExporterV1` (python-docx) to the same `PresentedReportV1`. No second DOCX content model. Body is editable text and tables, not PDF page images.

## Identity

`analysis_id` from G2-01R is `ReportInputV1.metadata.case_id`, the `X-BTE-Analysis-Id` download header, the PDF/DOCX footer, and DOCX document properties. Export does not invent a second id.

Current `/result` exports `source=current`. `?from=history&id=` exports that history row. A payload whose `data.analysis_id` disagrees with the request id is rejected.

## Dụng / Hỷ / Kỵ / Điều hậu

Customer Hỷ uses `favorable_display` (HK-R1H). Internal `favorable_gods` / `pattern.hy_than` are not shown as Hỷ. Điều hậu stays on its own rows (`Điều hậu ưu tiên` / climate), not merged into Overall Dụng.

## Tests

```
python -m pytest applications/api/tests/test_g2_04_customer_export.py applications/api/tests/test_g2_04_export_parity.py -q
npx vitest run tests/js/g2_04_customer_export.test.tsx
python release/gate_02/_g2_04_export_probe.py
```

- API/export: **10 passed**
- Portal: **5 passed** (G2-02 regression still **11 passed**)
- Probe: **10/10 MATCH**, `mismatch_count: 0`

## Performance baseline (representative, not optimized)

| Case | Official PDF | DOCX |
|------|----------------|------|
| Đặng Thị Dung (long) | 4.74 s | 0.53 s |
| Tuyền | 3.57 s | 0.18 s |
| Trường | 2.89 s | 0.18 s |
| Dũng | 7.90 s | 0.55 s |

## Diff audit (this phase)

Analytical engine / rule files changed: **0**.

Allowed: customer export adapter/service/routes, Report V1 presentation/CSS/PDF footer/DOCX properties, Portal export actions, tests, probe, freeze docs, Result bundle.

Deleted unused prior draft `applications/api/services/customer_report_adapter.py` in favor of `customer_report_input.py` (same role: stored JSON → `ReportInputV1`).

## Next

Do **not** start G2-05 automatically. G2-05 begins only after Product Owner accepts this freeze.
