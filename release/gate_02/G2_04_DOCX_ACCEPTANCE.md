# G2-04 — DOCX acceptance

## Path

Selected canonical analysis → `build_customer_report_input` → `ReportInputV1` → `build_presented_report` → existing `DocxExporterV1` (`python-docx`) → `POST /api/v1/export/docx`.

No second DOCX content model. PDF pages are not embedded as images.

## Parity with official PDF

Same `PresentedReportV1` sections. Layout may differ (DOCX uses Heading 1 + tables instead of CSS cards).

Required semantic parity (verified on Tuyền pytest + Dũng/Tuyền/Trường/Dung probe files):

- Four Pillars
- Strength score/class (`Điểm thân`)
- Pattern `cach_cuc` / qualification wording
- Điều hậu separate from Overall Dụng
- Phân bố Ngũ hành + structural disclaimer
- Ten Gods (visible / hidden entries when present)
- ShenSha canonical names
- Dụng display + Căn cứ chọn Dụng
- Customer Hỷ (`favorable_display`, HK-R1H)
- Kỵ
- Luck cycles
- G2-03 `pack05_narrative_result_v1` sections (not a generic chart essay)

## Editability

- Opens as OpenXML (`PK` zip, `[Content_Types].xml`)
- Paragraphs and table cells are real text (pytest reads **both**, avoiding the G1-02 paragraph-only miss)
- Vietnamese Unicode preserved (`Nguyễn`, `Thủy`, `Tuyền`)
- Core properties: title, subject, `identifier` = analysis id, comments with generated_at / BTE V1.0

## Customer action

Portal label: **Tải DOCX**. MIME:

`application/vnd.openxmlformats-officedocument.wordprocessingml.document`

`Content-Disposition: attachment` with RFC 5987 `filename*`. `X-BTE-Analysis-Id` set.

## Files

| Case | DOCX |
|------|------|
| Dũng | `screenshots/g2_04/BTE_BaoCao_Ngo_Đac_Dung_19850918_V1.docx` |
| Tuyền | `screenshots/g2_04/BTE_BaoCao_Vu_Thi_Thanh_Tuyen_19840713_V1.docx` |
| Trường | `screenshots/g2_04/BTE_BaoCao_Cao_Xuan_Truong_19890721_V1.docx` |
| Dung | `screenshots/g2_04/BTE_BaoCao_Đang_Thi_Dung_19820522_V1.docx` |

## Baseline time

0.18–0.55 s per case on this workstation. Not optimized.
