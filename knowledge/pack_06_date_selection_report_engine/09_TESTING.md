# PACK 06 — DATE SELECTION REPORT ENGINE

# 09_TESTING.md

**Status:** DRAFT → CANONICAL REVIEW  
**Pack:** PACK 06  
**Module:** Date Selection Report Engine  
**Version:** 1.0

---

# 1. PURPOSE

This document defines the canonical testing strategy for PACK 06.

The objective is to guarantee that:

- analytical truth is preserved
- reports are complete
- PDF and DOCX are consistent
- exports are deterministic
- future changes do not break existing behavior

Testing covers PACK 06 only.

Analytical correctness belongs to Date Selection Engine tests.

---

# 2. TESTING PHILOSOPHY

PACK 06 does **not** test astrology.

PACK 06 tests:

- data integrity
- report integrity
- rendering
- exporting
- regression
- user-visible output

Core rule:

> **Never test calculations twice. Test that calculations are preserved.**

---

# 3. TEST LAYERS

PACK 06 uses seven testing layers.

```text
Layer 1
Unit Tests

↓

Layer 2
Model Tests

↓

Layer 3
Adapter Tests

↓

Layer 4
Render Tests

↓

Layer 5
Export Tests

↓

Layer 6
Integration Tests

↓

Layer 7
Regression Tests
```

---

# 4. UNIT TESTS

Purpose:

Verify isolated components.

Components:

- Report Adapter
- Validators
- Filename generator
- Localization helpers
- Template loader
- Report metadata builder

No external dependencies.

---

# 5. DATA MODEL TESTS

Verify:

## Metadata

Required fields exist.

## Person

All mandatory fields exist.

## Search Period

Month/year preserved.

## Recommendation

All canonical fields preserved.

## Compatible Hours

All required fields preserved.

## Positive Times

Grouped correctly.

---

# 6. ADAPTER TESTS

Input:

```text
DateSelectionSearchResult
```

Output:

```text
DateSelectionReportModel
```

Verify:

- no recalculation
- no mutation
- no field loss
- recommendation order preserved

---

# 7. PERSON TESTS

Verify:

- name preserved
- gender preserved
- solar birthday preserved
- lunar birthday preserved
- Can Chi year preserved
- Nạp Âm preserved
- Cung preserved
- Trạch preserved

---

# 8. RECOMMENDATION TESTS

Verify every recommendation contains:

- solar date
- lunar date
- Can Chi year
- Can Chi month
- Can Chi day
- Day Result
- Nạp Âm
- Cung
- Trạch

No missing fields.

---

# 9. COMPATIBLE HOUR TESTS

Verify every compatible hour contains:

- branch
- time range
- Ganzhi
- Nạp Âm
- Cung
- Trạch

No "Hour Result".

---

# 10. POSITIVE TIME TESTS

Verify exported positive groups contain only:

- Đại An
- Tốc Hỷ
- Tiểu Cát

Reject:

- Lưu Liên
- Xích Khẩu
- Không Vong

---

# 11. TEMPLATE TESTS

Verify:

- every template loads
- every placeholder resolves
- no unresolved placeholders remain
- optional sections behave correctly

---

# 12. RENDER TESTS

Render:

- Header
- Person
- Search
- Recommendation
- Guidance
- Footer

Verify all sections appear.

---

# 13. PDF TESTS

Verify:

✓ PDF generated

✓ Unicode preserved

✓ Vietnamese labels preserved

✓ page count > 0

✓ recommendation order preserved

✓ no unresolved placeholders

---

# 14. DOCX TESTS

Verify:

✓ DOCX generated

✓ editable

✓ headings preserved

✓ Unicode preserved

✓ recommendation blocks preserved

---

# 15. EXPORT TESTS

Verify:

- filename generation
- MIME type
- output exists
- export duration
- repeated export consistency

---

# 16. LOCALIZATION TESTS

Verify public report uses Vietnamese.

Reject labels such as:

- Year Ganzhi
- Month Ganzhi
- Hour Result
- September

Expected:

- Can Chi năm
- Can Chi tháng
- Giờ phù hợp Nhóm Trạch của bạn
- Tháng 09/2026

---

# 17. FILE NAME TESTS

Verify:

PDF:

```text
bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.pdf
```

DOCX:

```text
bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.docx
```

ASCII filename.

Unicode document.

---

# 18. REPORT CONSISTENCY TESTS

Compare:

```text
SearchResult
```

↓

```text
ReportModel
```

↓

```text
PDF
```

↓

```text
DOCX
```

Verify identical analytical values.

---

# 19. GOLDEN DATASET

At least one frozen customer case.

Recommended:

```text
Nguyễn Tiến Sơn

Male

21/01/1987

09/2026
```

Verify:

- person block
- recommendation order
- compatible hours
- positive times

Golden data must come from Date Selection Engine.

Never hardcode report values independently.

---

# 20. MULTI-RECOMMENDATION TEST

Generate:

5 recommendations.

Verify:

- all rendered
- numbering correct
- no duplication
- no missing blocks

---

# 21. EMPTY RESULT TEST

If no suitable dates exist:

Verify report generation fails gracefully or displays the approved empty state.

No blank pages.

---

# 22. LONG NAME TEST

Example:

Very long Vietnamese name.

Verify:

- wrapping
- layout stability
- PDF
- DOCX

---

# 23. MULTI-PAGE TEST

Generate report exceeding one page.

Verify:

Recommendation blocks remain coherent.

No incorrect page split.

---

# 24. PERFORMANCE TEST

Generate reports repeatedly.

Verify:

No increasing memory usage.

No duplicated rendering.

No unnecessary recalculation.

---

# 25. CONCURRENCY TEST

Generate multiple reports simultaneously.

Verify:

- independent output
- no mixed customer data
- unique filenames

---

# 26. REGRESSION TESTS

After every change verify:

- Date Selection unchanged
- recommendation order unchanged
- compatible hours unchanged
- positive times unchanged

PACK 06 must never alter Date Selection behavior.

---

# 27. SECURITY TESTS

Verify:

No internal filesystem paths.

No stack traces.

No temporary filenames.

No private implementation details.

---

# 28. ACCEPTANCE TESTS

The following user journey must succeed:

```text
Search

↓

Top-5

↓

Export PDF

↓

Download

↓

Open PDF
```

Repeat for DOCX.

---

# 29. AUTOMATION

Recommended CI groups:

```text
unit

adapter

render

export

integration

regression
```

Failures in any required group block release.

---

# 30. TEST COVERAGE TARGETS

Recommended minimum coverage:

| Area | Target |
|------|-------:|
| Report Adapter | ≥95% |
| Validation | ≥95% |
| Templates | ≥90% |
| Render | ≥90% |
| Export | ≥90% |
| Integration | ≥90% |

Coverage targets are guidance.

Correctness has priority.

---

# 31. FAILURE POLICY

A failed:

- adapter
- validator
- render
- export
- regression

test blocks release.

No ignored failures.

---

# 32. TEST REPORT

Each execution should report:

- total tests
- passed
- failed
- skipped
- duration

Include separate counts for:

PDF

DOCX

Regression

---

# 33. ACCEPTANCE CRITERIA

PACK 06 testing PASS requires:

✓ Unit tests pass

✓ Model tests pass

✓ Adapter tests pass

✓ Render tests pass

✓ PDF tests pass

✓ DOCX tests pass

✓ Integration tests pass

✓ Regression tests pass

✓ Golden dataset passes

✓ No analytical mutation detected

---

# 34. SUMMARY

Testing verifies one invariant:

```text
Frozen SearchResult

↓

ReportModel

↓

RenderTree

↓

PDF

↓

DOCX
```

Every stage must preserve the same analytical truth.

Core principle:

> **Calculate once. Validate everywhere. Export with confidence.**

---

# STATUS

**READY FOR ARCHITECTURE REVIEW**