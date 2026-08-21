# G2-04 — PDF acceptance

## Policy

**OFFICIAL PDF** = Report V1 HTML (`render_html` / `PresentedReportV1`) printed by Playwright Chromium (`PdfExporterV1`).

**PRINT VIEW** = browser print of `/result` (or `/reports` preview). Convenience only. Must not be labeled as a second official PDF.

## Source

Official PDF does **not** scrape the Result DOM. It consumes the selected stored analysis through `customer_report_input` → `ReportInputV1` → `PresentedReportV1`.

## Layout freeze (polish only)

`engines/report_engine/templates/v1/report_v1.css`:

- A4, 16–20 mm margins (Playwright footer uses 20 mm bottom)
- Vietnamese-safe font stack: Segoe UI / Arial / Noto Sans
- Small cards (`page-break-inside: avoid`): profile, pillars, five elements, strength, pattern, useful god, shensha
- Long sections (`report-v1__section--flow`): narrative, luck table, recommendations, conclusion — allowed to split
- Headings keep `page-break-after: avoid`
- Meta values and table cells `overflow-wrap: anywhere`
- Pillars print as 2 columns

Playwright footer: `BTE V1.0` + page number / page count. Document footer also carries analysis id and generated time.

## Unicode / searchable

- HTML source is UTF-8 and contains Vietnamese Dụng / Hỷ strings (pytest + HTML fixtures).
- Generated PDF is a real `%PDF` with `/Font` (not image-only pages).
- Info Title extracts as UTF-16 (`Báo cáo Bát Tự — {name}`).
- Chromium CID body text is not reliably grepped as UTF-8; acceptance of body search is via HTML source + tagged print (`tagged=True`) + visual HTML/PNG/PDF files under `screenshots/g2_04/`.

## Visual files

`release/gate_02/screenshots/g2_04/`

| Case | Official HTML | PNG | PDF |
|------|---------------|-----|-----|
| Dũng | `dung_official.html` | `dung_official.png` | `BTE_BaoCao_Ngo_Đac_Dung_19850918_V1.pdf` |
| Tuyền | `tuyen_official.html` | `tuyen_official.png` | `BTE_BaoCao_Vu_Thi_Thanh_Tuyen_19840713_V1.pdf` |
| Trường | `truong_official.html` | `truong_official.png` | `BTE_BaoCao_Cao_Xuan_Truong_19890721_V1.pdf` |
| Dung (long) | `dungthi_official.html` | `dungthi_official.png` | `BTE_BaoCao_Đang_Thi_Dung_19820522_V1.pdf` |

Print view of `/result` is the G2-02 Result layout with chrome and the export bar hidden (`@media print`). Do not treat those prints as the official PDF.

## Baseline time

Dũng official PDF ~7.9 s; others 2.9–4.7 s on this workstation. Not optimized.

## Forbidden

- Browser DOM scrape as official PDF
- Two customer buttons both named “Xuất PDF”
- Image-only PDF
- Recomputing Dụng / Strength / Pattern in the renderer
