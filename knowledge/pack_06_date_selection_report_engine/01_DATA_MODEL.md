# PACK 06 — DATE SELECTION REPORT ENGINE

# 01_DATA_MODEL.md

**Status:** DRAFT → CANONICAL REVIEW  
**Pack:** PACK 06  
**Module:** Date Selection Report Engine  
**Version:** 1.0

---

# 1. PURPOSE

This document defines the canonical data model used by PACK 06.

The objective is to guarantee that:

- Date Selection Engine computes analytical truth exactly once.
- PACK 06 never recalculates analytical data.
- PDF and DOCX always render from the same canonical report model.
- Every exported report contains identical analytical facts regardless of format.

This document defines **data only**.

No rendering, business logic, or export implementation belongs here.

---

# 2. DESIGN PRINCIPLES

The data model follows five rules.

## Rule 1 — Single Source of Truth

All analytical data originates from:

```text
DateSelectionSearchResult
```

PACK 06 never computes:

- lunar calendar
- Can Chi
- Nạp Âm
- Cung Phi
- Đông/Tây Tứ Trạch
- six-state results
- compatible hours
- positive khắc

---

## Rule 2 — Immutable Report Input

Once the report adapter receives the search result:

```text
SearchResult
        ↓
ReportModel
```

No analytical value may change.

---

## Rule 3 — One Report Model

PDF

and

DOCX

must consume the same:

```text
DateSelectionReportModel
```

No format-specific analytical models.

---

## Rule 4 — Explicit Semantics

Every field has one meaning only.

Example:

```text
nayin
```

is never reused as

```text
cung_element
```

Likewise:

```text
cung
```

is never overloaded to mean

```text
trach_group
```

---

## Rule 5 — Human Readability

The report model is optimized for:

- report composition
- template binding
- validation
- testing

not database normalization.

---

# 3. ROOT MODEL

Canonical object:

```text
DateSelectionReportModel
```

Structure:

```text
DateSelectionReportModel
│
├── metadata
├── person
├── search_period
├── recommendations[]
├── guidance
└── provenance
```

---

# 4. METADATA

Purpose:

Describe the report itself.

Fields:

```text
metadata

report_id

report_schema_version

report_type

generated_at

locale

title

generator
```

Example:

```text
report_type

date_selection
```

Example title:

```text
BÁO CÁO CHỌN NGÀY TỐT
```

Metadata never influences analytical content.

---

# 5. PERSON REPORT DATA

Object:

```text
PersonReportData
```

Fields:

```text
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

Example:

```text
Họ tên

Nguyễn Tiến Sơn

Giới tính

Nam

Ngày sinh dương

21/01/1987

Ngày sinh âm

22/12/1986

Can Chi năm

Bính Dần

Nạp âm

Hỏa

Cung Phi

Khôn

Hành Cung

Thổ

Nhóm Trạch

Tây Tứ Trạch
```

---

# 6. PERSON INVARIANTS

Required:

```text
full_name

gender

birth_solar

birth_lunar

year_ganzhi

nayin

cung_phi

trach_group
```

Forbidden:

Missing lunar birthday.

Missing Cung Phi.

Missing Trạch group.

---

# 7. SEARCH PERIOD

Object:

```text
SearchPeriodReportData
```

Fields:

```text
month

year

display
```

Example:

```text
09

2026

09/2026
```

Customer label:

```text
Tháng tìm ngày tốt

09/2026
```

---

# 8. RECOMMENDATION COLLECTION

Object:

```text
RecommendationCollection
```

Contains:

```text
recommendations[]
```

Order is significant.

Order must equal Date Selection ranking.

No sorting inside PACK 06.

---

# 9. RECOMMENDED DAY

Object:

```text
RecommendedDateReportData
```

Fields:

```text
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

---

# 10. DAY SEMANTICS

Each field has exactly one meaning.

Example:

```text
nayin
```

Means:

Nạp Âm của Can Chi ngày.

Not:

Cung element.

Example:

```text
cung
```

Means:

Hạ Nguyên Cung của ngày.

Not:

Person Cung.

---

# 11. DAY RESULT

Allowed values:

```text
Đại An

Lưu Liên

Tốc Hỷ

Xích Khẩu

Tiểu Cát

Không Vong
```

Exactly one value.

---

# 12. COMPATIBLE HOURS

Object:

```text
CompatibleHourReportData
```

Fields:

```text
branch

time_range

ganzhi

nayin

cung

cung_element

trach_group

positive_ke[]
```

---

# 13. HOUR SEMANTICS

Important:

Hour does NOT contain:

```text
hour_result
```

There is no:

```text
Đại An

Tiểu Cát

...
```

attached to the hour itself.

Hour exists only to describe:

- Can Chi
- Nạp Âm
- Cung
- Hành Cung
- Trạch

Business rule:

```text
DAY

↓

Result

HOUR

↓

Compatibility

KHẮC

↓

Execution Time
```

---

# 14. POSITIVE KHẮC

Object:

```text
PositiveKeReportData
```

Fields:

```text
index

time_range

result
```

Allowed values:

```text
Đại An

Tốc Hỷ

Tiểu Cát
```

Only positive results are exported.

Negative classes:

```text
Lưu Liên

Xích Khẩu

Không Vong
```

are omitted from the report.

---

# 15. GUIDANCE

Object:

```text
GuidanceReportData
```

Purpose:

Educational explanation only.

Fields:

```text
title

items[]
```

Recommended items:

```text
Đại An

Tốc Hỷ

Tiểu Cát
```

Must never provide deterministic promises.

---

# 16. PROVENANCE

Object:

```text
ProvenanceData
```

Fields:

```text
source

search_result_id

generated_at

engine_version
```

Purpose:

Traceability.

Not shown to customer.

---

# 17. COMPLETE OBJECT GRAPH

```text
DateSelectionReportModel

metadata

person

search_period

recommendations[]

recommendation

compatible_hours[]

positive_ke[]

guidance

provenance
```

---

# 18. FIELD OWNERSHIP

Only one owner exists for each analytical field.

| Field | Owner |
|--------|-------|
| Solar birthday | Calendar Engine |
| Lunar birthday | Calendar Engine |
| Year Ganzhi | Calendar Engine |
| Month Ganzhi | Calendar Engine |
| Day Ganzhi | Calendar Engine |
| Nạp Âm | 60 Hoa Giáp |
| Cung Phi | Hạ Nguyên mapping |
| Hành Cung | Cung mapping |
| Trạch Group | Cung mapping |
| Day Result | Date Selection Engine |
| Compatible Hours | Date Selection Engine |
| Positive Khắc | Date Selection Engine |

PACK 06 owns none of these analytical values.

---

# 19. REPORT ADAPTER CONTRACT

Input:

```text
DateSelectionSearchResult
```

Output:

```text
DateSelectionReportModel
```

Adapter responsibilities:

- validate
- normalize
- format display values
- preserve canonical order

Adapter must not:

- calculate
- rerank
- reinterpret

---

# 20. VALIDATION RULES

The report model is invalid if:

Person:

- missing name
- missing gender
- missing birth dates
- missing Cung Phi

Recommendation:

- missing day_result
- missing Ganzhi
- missing Nạp Âm
- missing Trạch

Hour:

- missing branch
- missing Cung
- missing Trạch

Positive khắc:

- missing time
- missing result

Validation failure must stop report generation.

---

# 21. DATA CONSISTENCY

Mandatory invariants:

```text
report.person

==

search_result.person
```

```text
report.recommendations

==

search_result.recommendations
```

```text
compatible_hours

==

search_result.compatible_hours
```

```text
positive_ke

==

search_result.positive_ke
```

No analytical mutation permitted.

---

# 22. REPORT IMMUTABILITY

Once the report model has been built:

No renderer may:

- modify values
- reorder recommendations
- remove compatible hours
- merge positive khắc
- recompute dates

Renderers are read-only consumers.

---

# 23. VERSIONING

Current schema:

```text
1.0
```

Future schema changes must be versioned.

Backward compatibility must be explicit.

---

# 24. SUMMARY

PACK 06 introduces one canonical reporting object:

```text
DateSelectionReportModel
```

It is the single presentation model shared by:

- PDF
- DOCX

The governing principle remains:

> **Calculate once. Report many times.**

No analytical truth may be duplicated, recalculated, or altered inside PACK 06.

---

# STATUS

**READY FOR ARCHITECTURE REVIEW**