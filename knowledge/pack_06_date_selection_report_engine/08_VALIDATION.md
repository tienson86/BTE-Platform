# PACK 06 — DATE SELECTION REPORT ENGINE

# 08_VALIDATION.md

**Status:** DRAFT → CANONICAL REVIEW  
**Pack:** PACK 06  
**Module:** Date Selection Report Engine  
**Version:** 1.0

---

# 1. PURPOSE

This document defines the canonical validation rules for PACK 06.

Validation guarantees that every exported report:

- is complete
- is internally consistent
- matches the frozen Date Selection result
- never invents analytical values
- never exports corrupted or incomplete customer reports

Validation is mandatory before rendering.

---

# 2. VALIDATION PHILOSOPHY

PACK 06 validates **data integrity**, not astrology.

Examples:

✓ Person information exists.

✓ Recommendation order is preserved.

✓ Positive time slots exist.

✗ PACK 06 never checks whether Đại An is "correct."

That responsibility belongs to Date Selection Engine.

---

# 3. VALIDATION LAYERS

PACK 06 uses five validation layers.

```text id="gk2r4v"
Layer 1
Request Validation

↓

Layer 2
SearchResult Validation

↓

Layer 3
ReportModel Validation

↓

Layer 4
Render Validation

↓

Layer 5
Export Validation
```

Rendering begins only if every layer succeeds.

---

# 4. LAYER 1 — REQUEST VALIDATION

Validate incoming report request.

Required:

- report format
- canonical SearchResult reference
- authenticated session (if applicable)

Reject:

- missing format
- unsupported format
- missing SearchResult
- malformed request

---

# 5. LAYER 2 — SEARCHRESULT VALIDATION

Validate that Date Selection returned a usable canonical result.

Mandatory:

```text id="e6rq91"
Person

Search Period

Recommendations
```

The SearchResult must already be frozen.

PACK 06 never reconstructs it.

---

# 6. PERSON VALIDATION

Required fields:

```text id="zzxtiu"
full_name

gender

birth_solar

birth_lunar

year_ganzhi

nayin

cung_phi

trach_group
```

Failure:

Abort report generation.

Do not generate partially populated reports.

---

# 7. SEARCH PERIOD VALIDATION

Required:

```text id="4p4rj4"
month

year
```

Optional:

display label.

Reject invalid months:

0

13

etc.

---

# 8. RECOMMENDATION VALIDATION

At least one recommendation must exist.

Each recommendation requires:

```text id="ic3r0m"
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

Missing mandatory fields invalidate the report.

---

# 9. DAY RESULT VALIDATION

Allowed values:

```text id="f3mjlwm"
Đại An

Lưu Liên

Tốc Hỷ

Xích Khẩu

Tiểu Cát

Không Vong
```

No unknown values.

No empty strings.

---

# 10. CUNG VALIDATION

Allowed Cung:

```text id="6l4r89"
Khảm

Ly

Chấn

Tốn

Càn

Khôn

Cấn

Đoài
```

Reject unknown values.

---

# 11. TRẠCH VALIDATION

Allowed groups:

```text id="fvn03l"
Đông Tứ Trạch

Tây Tứ Trạch
```

Reject:

- empty
- unknown

---

# 12. NẠP ÂM VALIDATION

Required:

```text id="y5qfxu"
Mộc

Hỏa

Thổ

Kim

Thủy
```

No generic:

"Ngũ hành"

No ambiguous values.

---

# 13. COMPATIBLE HOUR VALIDATION

Each compatible hour requires:

```text id="qv3tdz"
branch

time_range

ganzhi

nayin

cung

trach_group

positive_ke
```

Reject incomplete hour blocks.

---

# 14. HOUR CONSISTENCY

Compatible hour must satisfy:

```text id="6jlwm6"
hour.trach_group

==

person.trach_group
```

Violation:

Validation failure.

Never export incompatible hours.

---

# 15. POSITIVE KHẮK VALIDATION

Every positive time requires:

```text id="7jlwm6"
index

time_range

result
```

Allowed results:

```text id="8jlwm6"
Đại An

Tốc Hỷ

Tiểu Cát
```

Reject:

- Lưu Liên
- Xích Khẩu
- Không Vong

inside exported positive-time groups.

---

# 16. DUPLICATE VALIDATION

Reject duplicate:

- recommendations
- compatible hours
- positive time slots

Duplicates indicate pipeline corruption.

---

# 17. ORDER VALIDATION

Recommendation order must equal:

```text id="9jlwm6"
SearchResult order
```

No reordering.

No sorting.

---

# 18. REPORT MODEL VALIDATION

After adapter:

Validate:

```text id="jlwm70"
Metadata

Person

Search Period

Recommendations

Guidance
```

The ReportModel must be complete before rendering.

---

# 19. TEMPLATE VALIDATION

Verify:

Every required placeholder resolves.

Example:

```text id="jlwm71"
{{person.full_name}}
```

must exist.

Missing mandatory placeholders:

Abort rendering.

---

# 20. RENDER VALIDATION

After Render Tree creation:

Verify:

Header

↓

Person

↓

Recommendations

↓

Footer

No missing mandatory sections.

---

# 21. EXPORT VALIDATION

Before export:

Verify:

Render Tree exists.

Output format supported.

Filename generated.

Metadata complete.

Abort export if invalid.

---

# 22. PDF VALIDATION

Verify:

- Unicode preserved
- page count > 0
- title rendered
- recommendations rendered
- no placeholder text remaining

---

# 23. DOCX VALIDATION

Verify:

- editable
- headings exist
- Unicode preserved
- recommendations exist
- placeholder text removed

---

# 24. ANALYTICAL IMMUTABILITY

Critical invariant:

```text id="jlwm72"
SearchResult

==

ReportModel

==

RenderTree

==

PDF

==

DOCX
```

Validation compares analytical fields.

Any mutation fails validation.

---

# 25. PERSON CONSISTENCY

Verify:

```text id="jlwm73"
Person in report

==

Person in SearchResult
```

Fields:

- name
- gender
- birthdays
- Cung
- Trạch

---

# 26. RECOMMENDATION CONSISTENCY

Verify:

```text id="jlwm74"
Recommendation count

Recommendation order

Recommendation values
```

Must match SearchResult.

---

# 27. HOUR CONSISTENCY

Verify:

Compatible hour list is unchanged.

No added hours.

No removed hours.

No reordered hours.

---

# 28. POSITIVE TIME CONSISTENCY

Verify:

Positive time list is unchanged.

No missing:

- Đại An
- Tốc Hỷ
- Tiểu Cát

if they exist in SearchResult.

---

# 29. LOCALIZATION VALIDATION

Verify customer-facing labels are Vietnamese.

Reject:

```text id="jlwm75"
Year Ganzhi

Hour Result

September
```

Expected:

```text id="jlwm76"
Can Chi năm

Tháng 09/2026

Giờ Thìn
```

---

# 30. FILE NAME VALIDATION

Verify:

ASCII filename.

Unicode report body.

Correct extension.

---

# 31. SECURITY VALIDATION

Ensure:

No internal paths.

No stack traces.

No temporary filesystem names.

No private diagnostics.

appear in exported documents.

---

# 32. PERFORMANCE VALIDATION

Typical report generation should not trigger:

Repeated analytical calculations.

Repeated SearchResult loading.

Repeated ReportModel creation.

---

# 33. FAILURE POLICY

Validation failure immediately aborts:

```text id="jlwm77"
Validation

↓

Stop

↓

Structured Error

↓

No Export
```

Never export partially validated reports.

---

# 34. VALIDATION RESULT

Canonical object:

```text id="jlwm78"
ValidationResult
```

Fields:

```text id="jlwm79"
status

errors[]

warnings[]

duration
```

Status:

PASS

FAIL

No intermediate states.

---

# 35. WARNING POLICY

Warnings may include:

- optional guidance missing
- optional metadata missing

Warnings never alter analytical truth.

---

# 36. ERROR POLICY

Errors include:

Missing person.

Missing recommendation.

Invalid Cung.

Invalid Trạch.

Invalid Nạp Âm.

Renderer failure.

Exporter failure.

Errors prevent export.

---

# 37. VALIDATION LOGGING

Log:

Validation started.

↓

Validation completed.

↓

PASS / FAIL.

Log only technical identifiers.

Avoid unnecessary personal information.

---

# 38. AUTOMATED VALIDATION TESTS

Test groups:

- request validation
- person validation
- recommendation validation
- hour validation
- positive time validation
- render validation
- export validation
- regression validation

---

# 39. ACCEPTANCE

Validation PASS when:

✓ Request valid.

✓ SearchResult valid.

✓ ReportModel complete.

✓ Recommendations complete.

✓ Compatible hours consistent.

✓ Positive times valid.

✓ Templates resolved.

✓ RenderTree valid.

✓ PDF valid.

✓ DOCX valid.

✓ No analytical mutation.

---

# 40. SUMMARY

Validation protects one invariant:

```text id="jlwm80"
Frozen SearchResult

↓

Validated ReportModel

↓

Validated RenderTree

↓

Validated PDF

↓

Validated DOCX
```

Core rule:

> **Nothing invalid is rendered. Nothing incomplete is exported. Nothing analytical is modified.**

---

# STATUS

**READY FOR ARCHITECTURE REVIEW**