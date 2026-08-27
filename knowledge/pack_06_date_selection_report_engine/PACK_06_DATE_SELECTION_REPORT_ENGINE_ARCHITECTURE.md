# PACK 06 — DATE SELECTION REPORT ENGINE ARCHITECTURE

**Status:** DRAFT → CANONICAL REVIEW  
**Version:** 1.0  
**Product:** BTE-Platform  
**Pack:** PACK 06 — Date Selection Report Engine  
**Scope:** Date Selection Report Generation only  
**Depends on:** Date Selection Engine V1.0 + PACK 05 Report Engine  
**Output:** PDF + DOCX  
**Language:** Vietnamese customer-facing output  
**Business Logic:** FROZEN — no Date Selection recalculation is permitted inside this Pack

---

# 1. PURPOSE

PACK 06 provides the canonical reporting layer for the BTE **Chọn ngày tốt** feature.

Its responsibility is to transform an already-computed canonical Date Selection result into professional, exportable customer reports.

The Pack does **not** calculate dates, hours, Cung Phi, Nạp Âm, Hạ Nguyên, Trạch group, or khắc.

Its responsibility begins only after Date Selection has produced a validated result.

Canonical flow:

```text
Date Selection Engine
        ↓
Canonical Search Result
        ↓
Date Selection Report Adapter
        ↓
DateSelectionReportModel
        ↓
Report Composition
        ↓
Render
        ↓
PDF / DOCX
```

PACK 06 must reuse the existing BTE report infrastructure wherever practical.

It must not create a second general-purpose report engine.

---

# 2. PRODUCT OBJECTIVE

A professional user should be able to:

```text
Enter customer information
        ↓
Search for suitable dates
        ↓
Review Top recommended dates
        ↓
Export report
        ↓
PDF / DOCX
```

The generated report must present the exact same canonical information shown in `/choose-date`.

No recomputation may occur during report generation.

---

# 3. CORE ARCHITECTURAL PRINCIPLE

## 3.1 One source of truth

The canonical Date Selection result is the only analytical input.

PACK 06 must not independently calculate:

- lunar date
- Can Chi
- Nạp Âm
- Cung Phi
- Hạ Nguyên Cung
- Hành Cung
- Đông/Tây Tứ Trạch
- day six-state result
- compatible hours
- six khắc
- positive time slots
- Top-5 ranking

These belong to the Date Selection Engine.

---

## 3.2 Report layer is presentation only

PACK 06 may:

- normalize display labels
- order sections
- paginate content
- construct report-specific view models
- apply typography
- apply report theme
- render PDF
- render DOCX

PACK 06 may not modify analytical truth.

---

# 4. SYSTEM BOUNDARIES

PACK 06 sits between:

```text
Date Selection
        ↓
PACK 06
        ↓
PACK 05 Report Infrastructure
```

Conceptually:

```text
┌────────────────────────────┐
│ Date Selection Engine V1.0 │
└──────────────┬─────────────┘
               │
               │ Canonical SearchResult
               ▼
┌────────────────────────────┐
│ PACK 06 Report Adapter     │
└──────────────┬─────────────┘
               │
               │ DateSelectionReportModel
               ▼
┌────────────────────────────┐
│ PACK 05 Report Runtime     │
│                            │
│ Layout                     │
│ Template                   │
│ Theme                      │
│ Render                     │
│ Export                     │
└───────────┬────────────────┘
            │
       ┌────┴────┐
       ▼         ▼
      PDF       DOCX
```

---

# 5. NON-GOALS

PACK 06 V1.0 must NOT implement:

- a new Date Selection algorithm
- new ranking rules
- weather
- tides
- Tiết khí scoring
- Đại Lục Nhâm
- event-specific date selection
- wedding-specific selection
- opening-business-specific calculation
- moving-house-specific calculation
- personalized AI interpretation
- new general Report Engine
- new PDF engine
- new DOCX engine

These may be future extensions.

---

# 6. SOURCE CONTRACT

The primary source must be the canonical Date Selection search result.

Conceptual input:

```text
DateSelectionSearchResult
```

Containing:

```text
person
search_period
recommendations[]
```

The report adapter must consume this object without recalculation.

---

# 7. CANONICAL REPORT MODEL

PACK 06 introduces:

```text
DateSelectionReportModel
```

Conceptual structure:

```text
DateSelectionReportModel
├── metadata
├── person
├── search_period
├── recommendations[]
├── guidance
└── provenance
```

---

# 8. REPORT METADATA

Recommended fields:

```text
metadata:
    report_id
    report_type
    schema_version
    generated_at
    locale
    title
```

Canonical values:

```text
report_type = "date_selection"
locale = "vi-VN"
title = "Báo cáo Chọn ngày tốt"
```

Report metadata must not affect calculations.

---

# 9. PERSON MODEL

Canonical report person block:

```text
person:
    full_name
    gender
    birth_solar
    birth_lunar
    year_ganzhi
    nayin
    cung_phi
    cung_element
    trach_group
```

Customer display:

```text
Họ và tên
Giới tính
Ngày sinh dương
Ngày sinh âm
Can Chi năm
Nạp âm
Cung Phi
Nhóm Trạch
```

Recommended compact presentation:

```text
Cung Phi: Khôn (Thổ)
Nhóm Trạch: Tây Tứ Trạch
```

Internally:

```text
cung_phi
cung_element
```

remain separate.

---

# 10. SEARCH PERIOD MODEL

```text
search_period:
    target_month
    target_year
    display_label
```

Example:

```text
08/2026
```

Customer-facing label:

```text
Tháng tìm ngày tốt: 08/2026
```

---

# 11. RECOMMENDATION MODEL

Each recommendation must preserve the canonical Date Selection result.

```text
recommendation:
    rank
    solar_date
    lunar_date
    year_ganzhi
    month_ganzhi
    day_ganzhi
    day_result
    nayin
    cung
    cung_element
    trach_group
    compatible_hours[]
```

No report-specific ranking may be applied.

The order must match Date Selection canonical ranking.

---

# 12. COMPATIBLE HOUR MODEL

```text
compatible_hour:
    branch
    full_time_range
    ganzhi
    nayin
    cung
    cung_element
    trach_group
    positive_ke[]
```

Customer presentation may remain compact:

```text
Giờ Thìn (07:01–09:00) · Càn (Kim)
```

The report must not show a six-state "hour result".

The approved business rule remains:

```text
DAY  → six-state classification
HOUR → Trạch compatibility
KHẮC → execution-time classification
```

---

# 13. POSITIVE KHẮC MODEL

```text
positive_ke:
    index
    time_range
    result
```

Allowed positive result values in the recommendation output:

```text
Đại An
Tốc Hỷ
Tiểu Cát
```

PACK 06 must not re-filter or recalculate them.

It simply receives validated positive time slots from Date Selection.

---

# 14. REPORT CONTENT STRUCTURE

The V1.0 report consists of four major sections.

---

## SECTION 01 — THÔNG TIN NGƯỜI XEM

Contents:

```text
Họ và tên
Giới tính
Ngày sinh dương
Ngày sinh âm
Can Chi năm
Nạp âm
Cung Phi
Nhóm Trạch
```

Purpose:

Provide a clear identity and personalization context.

---

## SECTION 02 — THÁNG TÌM NGÀY TỐT

Contents:

```text
Tháng tìm ngày tốt
Số ngày đề xuất
```

Optional short explanatory statement:

```text
Các ngày dưới đây được hệ thống lựa chọn theo dữ liệu cá nhân
và kết quả tính toán đã xác định.
```

Do not expose proprietary formulas.

---

## SECTION 03 — CÁC NGÀY ĐỀ XUẤT

This is the primary section of the report.

Each recommendation must show:

```text
Ngày dương
Ngày âm
Kết quả ngày

Can Chi năm
Can Chi tháng
Can Chi ngày

Nạp âm
Cung Phi
Nhóm Trạch

Giờ phù hợp Nhóm Trạch
Các thời điểm đẹp
```

Example visual concept:

```text
01
04/09/2026
23/07/2026 âm

ĐẠI AN

Can Chi năm:   Bính Ngọ
Can Chi tháng: Giáp Thân
Can Chi ngày:  Tân Tỵ

Nạp âm:        Kim
Cung Phi:      Cấn (Thổ)
Nhóm Trạch:    Tây Tứ Trạch

Giờ phù hợp Nhóm Trạch của bạn

• Giờ Thìn (07:01–09:00) · Càn (Kim)
• Giờ Tỵ   (09:01–11:00) · Khôn (Thổ)

Các thời điểm đẹp

Đại An
• ...

Tốc Hỷ
• ...

Tiểu Cát
• ...
```

Actual report data must always come from runtime canonical results.

---

# 15. SECTION 04 — HƯỚNG DẪN THAM KHẢO

V1.0 may contain a very short educational block explaining the positive classes.

Recommended:

```text
Đại An
Thiên về sự ổn định, bền vững và yên định.

Tốc Hỷ
Thiên về sự nhanh chóng, thuận lợi và tin vui.

Tiểu Cát
Thiên về sự thuận lợi, phát triển và cầu tài.
```

This section must be informational only.

It must not say:

```text
You must use Đại An for...
```

Preferred language:

```text
Có thể tham khảo...
Phù hợp với xu hướng...
Có thể ưu tiên khi...
```

No deterministic promises.

---

# 16. REPORT TITLE

Canonical title:

# BÁO CÁO CHỌN NGÀY TỐT

Optional subtitle:

```text
BTE — Date Selection Report
```

However, customer-facing output should prioritize Vietnamese.

---

# 17. PDF DESIGN PRINCIPLE

The PDF must be a structured report.

It must NOT be:

- a screenshot of `/choose-date`
- browser print of the live UI
- rasterized dashboard
- image-based report

It must use report templates.

---

# 18. PDF LAYOUT

Recommended:

```text
A4 Portrait
```

Primary structure:

```text
Cover / Header
↓
Person Information
↓
Search Period
↓
Recommended Date 1
↓
Recommended Date 2
↓
...
↓
Guidance
↓
Footer
```

Recommendations should avoid splitting critical blocks across pages where practical.

---

# 19. DOCX PRINCIPLE

DOCX must contain the same canonical content as PDF.

It must be:

- editable
- Unicode-safe
- Vietnamese-safe
- structured
- generated from the same report model

PDF and DOCX must never calculate separate truth.

---

# 20. SINGLE REPORT MODEL RULE

Critical invariant:

```text
DateSelectionReportModel
        ├── PDF
        └── DOCX
```

Forbidden:

```text
PDF Model
DOCX Model
```

with duplicated content derivation.

Both output formats must share one canonical report model.

---

# 21. PACK 05 REUSE

PACK 06 should reuse existing PACK 05 infrastructure wherever compatible.

Audit and reuse:

- report model conventions
- layout engine
- template loader
- theme engine
- render engine
- PDF export
- DOCX export
- output naming
- file delivery
- validation
- logging

PACK 06 is a domain-specific report package.

It is not another report platform.

---

# 22. REPORT ADAPTER

Introduce:

```text
DateSelectionReportAdapter
```

Responsibility:

```text
DateSelectionSearchResult
        ↓
validate
        ↓
normalize
        ↓
DateSelectionReportModel
```

It may:

- format dates for display
- organize sections
- combine Cung display as `Cấn (Thổ)`
- group positive khắc by result

It may not:

- rerank dates
- recalculate hours
- calculate Cung
- calculate Ganzhi
- calculate khắc

---

# 23. VALIDATION

Before rendering, validate:

## Person

Required:

```text
name
gender
birth_solar
birth_lunar
year_ganzhi
cung_phi
trach_group
```

## Recommendation

Required:

```text
solar_date
lunar_date
year_ganzhi
month_ganzhi
day_ganzhi
day_result
nayin
cung
trach_group
```

## Compatible hour

Required:

```text
branch
full_time_range
ganzhi
cung
trach_group
```

## Positive khắc

Required:

```text
time_range
result
```

Invalid analytical input must fail report generation.

PACK 06 must not invent fallback astrological values.

---

# 24. DATA CONSISTENCY INVARIANTS

Mandatory:

```text
report.person == source.person
```

```text
report.recommendations order == source.recommendations order
```

```text
report day_result == source day_result
```

```text
report compatible_hours == source compatible_hours
```

```text
report positive_ke == source positive_ke
```

No semantic mutation is allowed.

---

# 25. PUBLIC API

Recommended endpoints:

```text
POST /api/v1/date-selection/report
```

or format-specific endpoints consistent with current Report Engine:

```text
POST /api/v1/date-selection/report/pdf
POST /api/v1/date-selection/report/docx
```

Final route naming must follow repository conventions discovered during implementation audit.

Do not create incompatible parallel API patterns.

---

# 26. REQUEST MODEL

Preferred conceptual request:

```text
DateSelectionReportRequest
```

Containing either:

```text
search_result
format
```

or:

```text
date_selection_result_id
format
```

depending on existing BTE ResultStore/report patterns.

The implementation audit must determine the correct repository-native pattern.

---

# 27. RESPONSE MODEL

Conceptual:

```text
DateSelectionReportResponse
```

Fields may include:

```text
report_id
format
filename
mime_type
download_url / file response
created_at
```

Use existing BTE export conventions.

---

# 28. FILE NAMING

Recommended Vietnamese-safe filename:

```text
bao-cao-chon-ngay-tot_<customer-slug>_<MM-YYYY>.pdf
```

Example:

```text
bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.pdf
```

DOCX:

```text
bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.docx
```

Use normalized ASCII slug for filename only.

Report body keeps Vietnamese Unicode.

---

# 29. TEMPLATE ENGINE

Suggested template package:

```text
date_selection_report/
├── report.html
├── report.docx.py / docx renderer
├── sections/
│   ├── person
│   ├── search_period
│   ├── recommendation
│   └── guidance
└── styles/
```

Actual structure must follow existing PACK 05 conventions.

Do not create a new templating framework.

---

# 30. THEME

Reuse BTE report theme.

Preferred visual language:

- white background
- dark text
- BTE blue accents
- restrained Five Element badges
- subtle dividers
- commercial report typography
- A4-safe spacing

Do not make the report look like the live dashboard.

It should feel like a professional consultation document.

---

# 31. FIVE ELEMENT VISUALS

Where appropriate:

```text
Mộc  → green
Hỏa  → red/orange
Thổ  → earth/yellow
Kim  → gray/silver
Thủy → blue
```

These are semantic accents only.

The report must remain readable in grayscale printing.

---

# 32. REPORT PAGINATION

Recommendations should be treated as semantic blocks.

Avoid:

```text
Page N:
date identity

Page N+1:
compatible hours
```

when practical.

Recommended-date content should remain together or split at explicit section boundaries.

---

# 33. EXPORT PIPELINE

Canonical:

```text
SearchResult
      ↓
DateSelectionReportAdapter
      ↓
DateSelectionReportModel
      ↓
ReportValidator
      ↓
Template/Layout
      ↓
Renderer
      ↓
Exporter
      ↓
PDF / DOCX
```

---

# 34. FAILURE BEHAVIOR

Report generation must fail clearly when:

- Date Selection result is missing
- person data is incomplete
- recommendations are invalid
- canonical analytical fields are missing
- renderer fails
- export fails

Never silently produce a report with fabricated data.

---

# 35. LOGGING

Log:

- report generation request
- report type
- source result identifier
- output format
- success/failure
- duration
- validation errors

Do not log unnecessary private personal information.

---

# 36. TESTING STRATEGY

PACK 06 requires four test layers.

## Unit

Test:

- Report Adapter
- Report Model
- Validator
- section builders
- filename generator

## Contract

Verify:

```text
SearchResult
→ ReportModel
```

without analytical mutation.

## Render

Verify:

- HTML
- PDF
- DOCX
- Vietnamese Unicode
- Five Element labels
- Top recommendations

## Integration

Verify:

```text
Date Selection search
→ report
→ PDF
→ DOCX
```

---

# 37. GOLDEN TEST CASE

Use at least one frozen Date Selection case.

Recommended:

```text
Name:
Nguyễn Tiến Sơn

Gender:
male

Birth:
21/01/1987

Target month:
09/2026
```

Use the canonical runtime result, not hardcoded fabricated recommendations.

Golden assertions must verify:

- person block
- lunar birthday
- year Ganzhi
- Nạp Âm
- Cung Phi
- Trạch
- recommended-day order
- compatible-hour data
- positive khắc data

---

# 38. PDF/DOCX CONSISTENCY TEST

Mandatory:

For the same `DateSelectionReportModel`:

```text
PDF content
```

and:

```text
DOCX content
```

must contain the same analytical facts.

Formatting may differ.

Truth may not.

---

# 39. PORTAL INTEGRATION

Recommended location:

`/choose-date`

After results are generated, provide export actions:

```text
Xuất PDF
Xuất DOCX
```

These actions must use the current search result.

They must not rerun Date Selection with potentially different runtime state unless repository architecture explicitly requires canonical result retrieval.

---

# 40. REPORT BUTTON RULE

Disable export when:

- no search has been run
- no recommendations exist
- result is invalid

Enable after canonical Date Selection result exists.

---

# 41. SECURITY / PRIVACY

Report output contains personal information.

Do not:

- expose reports to unrelated users
- use predictable public report URLs without access control
- log birth data unnecessarily
- persist reports indefinitely unless existing BTE policy requires it

Follow current BTE report/file policies.

---

# 42. VERSIONING

PACK 06 V1.0 should version:

```text
DateSelectionReportModel
Template
Schema
```

Recommended:

```text
report_schema_version = "1.0"
```

Future report presentation changes must not silently reinterpret old canonical results.

---

# 43. DOCUMENT TREE

Canonical documentation target:

```text
knowledge/
└── pack_06_date_selection_report_engine/
    ├── PACK_06_DATE_SELECTION_REPORT_ENGINE_ARCHITECTURE.md
    ├── 01_DATA_MODEL.md
    ├── 02_RUNTIME_PIPELINE.md
    ├── 03_PUBLIC_API.md
    ├── 04_REPORT_LAYOUT.md
    ├── 05_RENDER_ENGINE.md
    ├── 06_EXPORT_ENGINE.md
    ├── 07_TEMPLATE_ENGINE.md
    ├── 08_VALIDATION.md
    ├── 09_TESTING.md
    └── 10_ACCEPTANCE.md
```

---

# 44. IMPLEMENTATION PHASES

After architecture freeze:

## P6-01

Report Data Model

## P6-02

Date Selection → Report Adapter

## P6-03

Report Layout + Template

## P6-04

PDF Renderer Integration

## P6-05

DOCX Renderer Integration

## P6-06

Portal Export Actions

## P6-07

Validation + Tests

## P6-08

Commercial Report Polish

## P6-09

Final Freeze

Do not implement later phases before their dependencies are complete.

---

# 45. ACCEPTANCE CRITERIA

PACK 06 V1.0 is PASS only if:

1. Date Selection analytical logic is not duplicated.
2. One canonical report model feeds PDF and DOCX.
3. Person information is correct.
4. Solar/lunar dates are correct.
5. Can Chi data matches Date Selection.
6. Nạp Âm is preserved.
7. Cung Phi is preserved.
8. Trạch group is preserved.
9. Top recommended dates preserve canonical order.
10. Compatible hours are preserved.
11. Positive time slots are preserved.
12. No `Kết quả giờ` is introduced.
13. PDF renders Vietnamese correctly.
14. DOCX renders Vietnamese correctly.
15. PDF and DOCX contain identical analytical facts.
16. Portal export works from `/choose-date`.
17. Existing Bazi reports remain unchanged.
18. Existing Date Selection results remain unchanged.
19. Automated tests pass.
20. No analytical formula is exposed publicly.

---

# 46. FREEZE POLICY

After PACK 06 Final Freeze:

Allowed:

- bug fixes
- typography corrections
- PDF pagination fixes
- DOCX layout fixes
- accessibility improvements
- non-semantic visual polish

Not allowed without version change:

- analytical recalculation
- ranking changes
- new Date Selection rules
- reinterpretation of Cung/Hạ Nguyên
- new khắc rules
- different PDF vs DOCX truth
- hidden fallback calculations

---

# 47. CANONICAL SUMMARY

PACK 06 is a **reporting package**, not an analytical engine.

Its canonical contract is:

```text
Date Selection Engine
        ↓
Frozen analytical truth
        ↓
DateSelectionReportAdapter
        ↓
DateSelectionReportModel
        ↓
PACK 05 reporting infrastructure
        ↓
PDF / DOCX
```

The fundamental invariant is:

> **Calculate once. Report many times.**

PDF and DOCX are views of the same canonical Date Selection result.

They are never independent analytical products.

---

# 48. ARCHITECTURE FREEZE GATE

Before implementation begins, confirm:

- Date Selection V1.0 is frozen.
- PACK 05 report infrastructure has been audited.
- Existing PDF exporter is reusable.
- Existing DOCX exporter is reusable.
- canonical Date Selection SearchResult is available.
- no analytical calculation is required inside PACK 06.

Only after these conditions are verified may P6-01 implementation begin.

---

# FINAL ARCHITECTURAL DECISION

**PACK 06 — Date Selection Report Engine V1.0**

Purpose:

> Convert frozen Date Selection results into professional PDF and DOCX reports using the existing BTE reporting infrastructure.

Core rule:

> **No recalculation. No duplicated truth. No independent PDF/DOCX logic.**

Status:

**READY FOR ARCHITECTURE REVIEW**