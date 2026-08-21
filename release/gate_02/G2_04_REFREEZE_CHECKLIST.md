# G2-04 — Refreeze checklist

Use after Product Owner accepts this freeze. Do **not** unfreeze Gate-1 engines to “fix” PDF/DOCX.

## Confirm before freeze

- [x] One canonical presentation model: stored analysis → `ReportInputV1` → `PresentedReportV1`
- [x] Official PDF is Report V1 Playwright, not browser Print-to-PDF
- [x] Print path labeled **In**, not a second “Xuất PDF”
- [x] Customer **Tải DOCX** uses existing python-docx renderer
- [x] PDF/DOCX share analytical truth with Result / Full Report
- [x] Canonical `analysis_id` retained (payload, footer, `X-BTE-Analysis-Id`)
- [x] Current vs History export isolated
- [x] Dụng reason visible
- [x] Hỷ HK-R1H (`favorable_display`) preserved
- [x] Kỵ unchanged vs stored payload
- [x] Điều hậu separate from Overall
- [x] Five Elements title + structural disclaimer
- [x] Pattern qualification / LEVEL-1 detected wording (no “Chuyên cách ưu tiên Ấn” on override=false)
- [x] Ten Gods from stored `ten_gods` (Nhật Chủ on day stem)
- [x] ShenSha canonical names, aliases not doubled in customer table
- [x] Luck from frozen G1-08 sequence on the selected analysis
- [x] PDF Unicode in title + `/Font` (not image-only)
- [x] DOCX Unicode + editable paragraphs **and** tables
- [x] No legacy HTML/MD/commercial PDF fallback for fresh `@1.5` results
- [x] Error states: 409/422/500 customer copy, no empty file
- [x] Ten control cases 0 analytical diffs
- [x] Visual HTML/PNG/PDF/DOCX under `release/gate_02/screenshots/g2_04/`
- [x] Analytical engine/rule files changed this phase: **0**

## Contracts frozen

- Analysis / customer: `analysis_result.UsefulGodView@1.5`
- Narrative: `pack05_narrative_result_v1`
- Presentation: `report.customer.PresentedReportV1@1.0`
- Report file: `report.customer.v1` / Report V1 `1.0`

## File naming

`BTE_BaoCao_{AsciiSlug}_{YYYYMMDD}_V1.{pdf|docx}`

Examples:

- `BTE_BaoCao_NgoDacDung_19850918_V1.pdf`
- `BTE_BaoCao_Vu_Thi_Thanh_Tuyen_19840713_V1.docx`

Analysis id is **not** the entire filename. It lives in metadata/footer/headers.

## Do not refreeze as Gate-1 truth

- Browser Print PDF
- Preview fixture (`?preview=1`)
- Legacy `/result?legacy=1`
- Commercial / simple PDF helpers
- Unstructured stored `report.html` / markdown

## Next gate

G2-05 starts only after Product Owner accepts G2-04. This checklist does not auto-start G2-05.
