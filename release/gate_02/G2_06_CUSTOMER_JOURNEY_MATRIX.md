# G2-06 — Customer journey matrix

Harness: `POST /api/v1/analyze` → stored snapshot → Result boot / Report V1 / official PDF / DOCX / History selection. Portal UI gates in vitest.

| # | Step | Sơn | Tuyền | Dũng | Trường | Notes |
|---|------|-----|-------|------|--------|-------|
| 1 | Open Analyze | PASS | PASS | PASS | PASS | Form fields: name, place, date, time, Nam/Nữ, timezone |
| 2 | Enter birth | PASS | PASS | PASS | PASS | Control-case births; place `Hà Nội` |
| 3 | Submit once | PASS | PASS | PASS | PASS | `analyzing` guard + disabled button |
| 4 | Analyze succeeds | PASS | PASS | PASS | PASS | Envelope `success` + `request_id` |
| 5 | Arrive at /result | PASS | PASS | PASS | PASS | Portal assigns `/result` after save |
| 6 | Read core result | PASS | PASS | PASS | PASS | Tứ trụ, Strength, Pattern, Dụng, Hỷ, Kỵ, Điều hậu |
| 7 | Open Luận giải | PASS | PASS | PASS | PASS | Same payload; no second Analyze |
| 8 | Open Full Report | PASS | PASS | PASS | PASS | `PresentedReportV1` from stored data |
| 9 | Tải PDF | PASS | PASS | PASS | PASS | `%PDF-` Playwright Report V1 |
| 10 | Tải DOCX | PASS | PASS | PASS | PASS | ZIP + Unicode paragraphs/tables |
| 11 | In | PASS | PASS | PASS | PASS | Label **In**; hint distinguishes official PDF |
| 12 | History row written | PASS | PASS | PASS | PASS | One row per successful Analyze |
| 13 | Open saved History | PASS | PASS | PASS | PASS | Explicit `?from=history&id=` |
| 14 | Report from History | PASS | — | PASS | — | Dũng History while current is Tuyền |
| 15 | Export History again | PASS | — | PASS | — | Filename/content of selected A |
| 16 | Return to current | PASS | PASS | PASS | PASS | `/result` without History query |
| 17 | Refresh | PASS | PASS | PASS | PASS | G2-05: no extra History row |
| 18 | Re-analyze | — | — | PASS | — | New id; old snapshot unchanged |

## Failure / safety rows (not case-specific)

| Step | Result |
|------|--------|
| Invalid input (API year=0) | 422, no stack, no fake payload |
| Required-field copy on form | Vietnamese (`Cần nhập họ và tên.` …) |
| Empty current `/result` | Empty gate + Analyze CTA |
| Missing History id | Không tìm thấy hồ sơ |
| Corrupt History | Safe error, not current |
| Old contract | Reanalyze/update notice |
| Narrow viewport (390×844) | Dũng report capture usable |

## Analytical coverage of the four

| Case | Strength | Pattern | Dụng | Reason | Hỷ | Điều hậu |
|------|----------|---------|------|--------|----|----------|
| Sơn | 0.87 strong | Chính Ấn | Hỏa · Đinh · Chính Quan | CHẾ | insufficient | Hỏa |
| Tuyền | 0.66 strong | Kiếp Tài | Mộc · Ất · Chính Quan | CHẾ | insufficient | Thủy |
| Dũng | 1.00 strong | Giá Sắc LEVEL-1, override false | Thủy · Nhâm · Thực Thần | TIẾT | insufficient | Hỏa |
| Trường | 0.34 weak | Quan Ấn tương sinh | Kim · Tân · Chính Ấn | SINH / TRỢ | Thủy · Nhâm · Tỷ Kiên | Thủy |
