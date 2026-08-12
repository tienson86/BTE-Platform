# CASE-0001 — Before / After WP-RPT-003A

**Before:** WP-RPT-003 artifacts  
**After:** WP-RPT-003A normalized HTML / PDF / DOCX  

Same source: `tests/golden_dataset/report_v1/CASE-0001/` + `build_case_0001_source()` → `ReportInputV1`.

---

## Artifact paths

| Role | Path |
|------|------|
| Before HTML | `knowledge/report_v1_validation/wp_rpt_003_baseline/CASE-0001.html` |
| Before PDF | `knowledge/report_v1_validation/wp_rpt_003_baseline/BTE_CASE-0001_Nguyen_Tien_Son_Report_V1_0.pdf` |
| Before DOCX | `knowledge/report_v1_validation/wp_rpt_003_baseline/BTE_CASE-0001_Nguyen_Tien_Son_Report_V1_0.docx` |
| After HTML | `knowledge/report_v1_validation/previews/CASE-0001.html` |
| After PDF | `knowledge/report_v1_validation/exports/BTE_CASE-0001_Nguyen_Tien_Son_Report_V1_0.pdf` |
| After DOCX | `knowledge/report_v1_validation/exports/BTE_CASE-0001_Nguyen_Tien_Son_Report_V1_0.docx` |

---

## ISSUE-001 — Internal values

| Field | Before | After |
|-------|--------|-------|
| Giới tính | `male` | `Nam` |
| Thân vượng mức | `strong` | `Thân vượng` |
| Cách cục trạng thái | `success` | `Đắc cách` |
| Điều hậu nhiệt | `hot` | `Nhiệt` |
| Thần sát loại | `shensha` | `Thần sát` |

`ReportInputV1` still stores internal codes. Localization happens in `engines/report_engine/localization/`.

---

## ISSUE-002 — Object leakage

| Field | Before | After |
|-------|--------|-------|
| Tiết khí | `{'name': 'Đại Hàn', 'index': 23}` | `Đại Hàn` |

---

## ISSUE-005 — Rule Engine text vs conclusion

**Before (10. Luận giải tổng thể):**

```text
Áp dụng bảng trạng thái ngũ hành của mùa đã được xác định.
Ưu tiên xác định mùa theo Tiết khí nếu dữ liệu Tiết khí có sẵn.
Nếu chưa có Tiết khí thì xác định mùa theo Địa Chi tháng.
...
Kích hoạt khi xác định Chính Cách.
Kích hoạt khi tháng sinh thuộc mùa Đông.
Tổng quan: Nhật Chủ Canh, cách cục Chinh An.
```

**After:**

```text
Tổng quan: Nhật Chủ Canh, cách cục Chinh An.
```

Instructional sentences dropped. Remaining sentence is from the interpretation library, not rewritten.

**17. Tổng kết**

| Before | After |
|--------|-------|
| Last section (`weakness`): `Yếu tố hao/khắc: Bị Quan Sát khắc.` | Section `conclusion`: `Điểm tổng hợp: 51.25 — hạng D+.` |

---

## ISSUE-004 / 008 / 009 / 010 — Runtime gaps

| Section | Before | After |
|---------|--------|-------|
| 03. Ngũ hành | Empty table (`—` × 5) | `DATA NOT PROVIDED BY RUNTIME` |
| 09. Đại vận | Current decade only, empty direction dl | Current decade + note: full cycles `DATA NOT PROVIDED BY RUNTIME` |
| 10. Luận giải tổng thể | Rule text dump / first-section fallback | Filtered summary; else `Chưa có dữ liệu tổng hợp.` |
| 12. Tài vận | `Chưa đủ dữ liệu để đưa ra kết luận.` | `DATA NOT PROVIDED BY RUNTIME` |
| 15. Tử tức | `Chưa đủ dữ liệu để đưa ra kết luận.` | `DATA NOT PROVIDED BY RUNTIME` |

No values invented.

---

## ISSUE-006 — ShenSha

Unchanged list (8 names). Duplicate candidates documented, not merged:

- Thiên Ất / Thiên Ất Quý Nhân
- Thiên Đức / Thiên Đức Quý Nhân
- Nguyệt Đức / Nguyệt Đức Quý Nhân

---

## ISSUE-007 — Semantic equality

HTML, PDF (from HTML), and DOCX now share `build_presented_report()`.

Fields restored in DOCX to match HTML:

- Trường sinh
- Pattern confidence (`Độ tin cậy`)
- Strength seasonal support / root
- Useful-god temperature
- Calendar mode (when present)
- Luck direction / start age / start date (when present)

---

## Unchanged professional content (by design)

- Pillars: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần
- Dụng thần / Hỷ thần / Kỵ thần values
- Strength score 0.87
- Pattern Chính Ấn
- Useful-god reasoning `Than vượng cần tiết khí` (upstream wording)
- `Chinh An` spelling in the kept summary sentence (upstream wording)
