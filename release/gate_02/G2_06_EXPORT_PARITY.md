# G2-06 — Export parity

Canonical path (G2-04, unchanged):

```
Stored Analyze JSON (UsefulGodView@1.5 + pack05_narrative_result_v1)
  → prepare_customer_report_input
  → ReportInputV1 → PresentedReportV1
  → HTML / Playwright PDF / DocxExporterV1
```

No second Analyze. No engine rescoring.

## Ten control cases — API / Result / Report model

Required: **MATCH**. Probe `ten_match: true`, `mismatch_count: 0`.

| Case | API+Result Dụng | Report Dụng | Hỷ | Surfaces |
|------|-----------------|-------------|-----|----------|
| Nguyễn Tiến Sơn | Hỏa · Đinh · Chính Quan | same | insufficient | MATCH |
| Lương Ngọc Huỳnh | Kim · Tân · Chính Tài | same | insufficient | MATCH |
| Đặng Thị Dung | Thủy · Nhâm · Chính Ấn | same | Mộc · Ất · Tỷ Kiên | MATCH |
| Đoàn Quang Hưng | Thủy · Nhâm · Chính Tài | same | insufficient | MATCH |
| Vũ Thị Thanh Tuyền | Mộc · Ất · Chính Quan | same | insufficient | MATCH |
| Cao Xuân Trường | Kim · Tân · Chính Ấn | same | Thủy · Nhâm · Tỷ Kiên | MATCH |
| Lưu Hoàng Sơn | Mộc · Ất · Chính Tài | same | insufficient | MATCH |
| Phạm Thị Huyền | Kim · Tân · Thực Thần | same | insufficient | MATCH |
| Lương Văn Mạnh | Kim · Tân · Thực Thần | same | insufficient | MATCH |
| Ngô Đắc Dũng | Thủy · Nhâm · Thực Thần | same | insufficient | MATCH |

## Primary four — PDF / DOCX / History

| Case | PDF exists / MIME | DOCX exists / ZIP | DOCX key strings | HTML key strings | History export |
|------|-------------------|-------------------|------------------|------------------|----------------|
| Sơn | PASS (173284 bytes) | PASS | PASS | PASS | n/a (trace only) |
| Tuyền | PASS | PASS | PASS | PASS | Current B |
| Dũng | PASS | PASS | PASS | PASS | History A isolated |
| Trường | PASS | PASS | PASS | PASS | n/a (trace only) |

DOCX is editable (python-docx paragraphs + table cells), Unicode correct, not image-only.

## File isolation

| Check | Result |
|-------|--------|
| Dũng DOCX contains Dũng Dụng | PASS |
| Dũng DOCX does not contain Tuyền Dụng | PASS |
| Tuyền DOCX contains Tuyền Dụng | PASS |
| Tuyền DOCX does not contain Giá Sắc | PASS |
| Distinct PDF filenames | PASS |

## PDF text search

Playwright CID fonts: naive UTF-8/UTF-16 grep of the `.pdf` bytes does **not** find Vietnamese strings. This matches G2-04 `pdf_searchable: false`. Visual HTML + DOCX are the inspectable text. Official PDF remains Report V1 Playwright, not browser Print.

## Customer-safe wording (HTML + DOCX)

After stripping `pat_ca_01` from pattern evidence at the customer report adapter:

- no rule IDs
- no `male` / `female`
- no `mock` / `fixture` / `undefined` / `null`
- no `UsefulGodView@1.5` in customer HTML/DOCX
