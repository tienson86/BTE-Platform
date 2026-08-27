# PACK 06 — DATE SELECTION REPORT ENGINE

# 10_ACCEPTANCE.md

**Status:** DRAFT → CANONICAL REVIEW  
**Pack:** PACK 06  
**Module:** Date Selection Report Engine  
**Version:** 1.0

---

# 1. PURPOSE

This document defines the canonical acceptance criteria for PACK 06.

A PACK is considered complete only when **all mandatory acceptance criteria are satisfied**.

Passing unit tests alone is **not** sufficient.

The implementation must satisfy:

- architecture
- runtime
- API
- rendering
- export
- user workflow
- regression

---

# 2. ACCEPTANCE PHILOSOPHY

PACK 06 is accepted only if it proves that:

> **One Date Selection result can be exported into professional PDF and DOCX reports without changing analytical truth.**

Everything else is secondary.

---

# 3. ACCEPTANCE LEVELS

PACK 06 uses four acceptance levels.

```text id="l0pn7g"
Level 1
Architecture

↓

Level 2
Technical

↓

Level 3
Commercial

↓

Level 4
Release
```

Every level must pass.

---

# 4. LEVEL 1 — ARCHITECTURE

The following must be verified.

## A1

One canonical Report Model.

PASS:

```text id="6sjbvt"
SearchResult

↓

DateSelectionReportModel
```

FAIL:

Different report models for PDF and DOCX.

---

## A2

No duplicated analytical engine.

PASS:

PACK 06 never recalculates Date Selection.

---

## A3

Report Adapter exists.

PASS:

SearchResult

↓

ReportModel

---

## A4

Render Engine reused.

PASS.

---

## A5

Export Engine reused.

PASS.

---

# 5. LEVEL 2 — TECHNICAL

## T1

Report request succeeds.

---

## T2

Report validation succeeds.

---

## T3

Render succeeds.

---

## T4

PDF generated.

---

## T5

DOCX generated.

---

## T6

Download succeeds.

---

## T7

No runtime exceptions.

---

## T8

No unresolved template placeholders.

---

## T9

Unicode preserved.

---

## T10

No analytical mutation.

---

# 6. LEVEL 3 — COMMERCIAL

The report must satisfy customer expectations.

---

## C1

Professional appearance.

---

## C2

Easy to read.

---

## C3

Clear hierarchy.

---

## C4

Customer information complete.

---

## C5

Recommendations understandable.

---

## C6

Compatible hours understandable.

---

## C7

Positive times understandable.

---

## C8

No internal algorithm exposed.

Examples that must NOT appear:

- modulo
- remainder
- Tiểu Lục Nhâm calculation
- Hạ Nguyên lookup rules
- internal ranking score

---

## C9

Vietnamese language throughout.

---

## C10

Printable.

---

# 7. LEVEL 4 — RELEASE

Release checklist.

---

## R1

Architecture approved.

---

## R2

All required documents completed.

---

## R3

Implementation complete.

---

## R4

Automated tests pass.

---

## R5

Manual verification passes.

---

## R6

Regression passes.

---

## R7

Product Owner approval obtained.

---

# 8. PERSON ACCEPTANCE

Report must contain:

✓ Họ và tên

✓ Giới tính

✓ Ngày sinh dương

✓ Ngày sinh âm

✓ Can Chi năm

✓ Nạp Âm

✓ Cung Phi

✓ Nhóm Trạch

No missing mandatory field.

---

# 9. SEARCH ACCEPTANCE

Report must contain:

✓ Tháng tìm ngày tốt

✓ Number of recommendations

---

# 10. RECOMMENDATION ACCEPTANCE

Every recommendation must contain:

✓ Ngày dương

✓ Ngày âm

✓ Kết quả ngày

✓ Can Chi năm

✓ Can Chi tháng

✓ Can Chi ngày

✓ Nạp Âm

✓ Cung Phi

✓ Nhóm Trạch

---

# 11. HOUR ACCEPTANCE

Every recommendation must contain:

✓ Giờ phù hợp Nhóm Trạch của bạn

Each compatible hour must show:

✓ Giờ Chi

✓ Khung giờ

✓ Cung (Element)

No "Kết quả giờ".

---

# 12. POSITIVE TIME ACCEPTANCE

Positive time section must exist.

Allowed groups:

✓ Đại An

✓ Tốc Hỷ

✓ Tiểu Cát

No negative classifications exported.

---

# 13. PDF ACCEPTANCE

PDF must:

✓ Open successfully.

✓ Preserve Unicode.

✓ Preserve recommendation order.

✓ Preserve positive times.

✓ Preserve person information.

---

# 14. DOCX ACCEPTANCE

DOCX must:

✓ Open successfully.

✓ Be editable.

✓ Preserve recommendation order.

✓ Preserve Unicode.

---

# 15. CONSISTENCY ACCEPTANCE

The following must always be identical:

```text id="l7a7nd"
SearchResult

↓

ReportModel

↓

PDF

↓

DOCX
```

Analytical content must never diverge.

---

# 16. LOCALIZATION ACCEPTANCE

The report must use Vietnamese labels.

Required:

- Can Chi năm
- Can Chi tháng
- Can Chi ngày
- Giờ phù hợp Nhóm Trạch của bạn
- Các thời điểm đẹp

Forbidden:

- Year Ganzhi
- Hour Result
- September
- Generic "Ngũ hành" when a more precise label is required

---

# 17. PERFORMANCE ACCEPTANCE

Typical report generation:

✓ No repeated calculations

✓ One adapter pass

✓ One render pass

✓ One export pass

No unnecessary duplication.

---

# 18. REGRESSION ACCEPTANCE

The following modules must remain unchanged:

✓ Calendar Engine

✓ Date Selection Engine

✓ Bazi Engine

✓ Interpretation

✓ Report Engine (existing)

✓ ResultStore

---

# 19. GOLDEN DATASET ACCEPTANCE

At least one frozen customer case must pass.

Recommended:

```text id="g2sk9y"
Nguyễn Tiến Sơn

21/01/1987

09/2026
```

The report must match the frozen SearchResult exactly.

---

# 20. MANUAL QA CHECKLIST

Reviewer verifies:

- Report title
- Person information
- Search period
- Recommendation order
- Compatible hours
- Positive times
- Guidance
- Footer
- PDF
- DOCX

No visual corruption.

---

# 21. PRODUCTION CHECKLIST

Before release:

□ Architecture approved

□ Documentation complete

□ Implementation complete

□ Tests passing

□ Manual QA complete

□ Screenshots archived

□ PDF archived

□ DOCX archived

□ Product Owner approval

---

# 22. RELEASE GATE

PACK 06 must NOT be released if:

- ReportModel is incomplete
- PDF differs from DOCX analytically
- Date Selection is recalculated
- Recommendation order changes
- Compatible hours change
- Positive times change
- Mandatory tests fail

---

# 23. FREEZE POLICY

After PACK 06 passes acceptance:

Allowed:

- bug fixes
- typography
- spacing
- pagination
- accessibility
- localization typo corrections

Not allowed:

- analytical recalculation
- new ranking rules
- different PDF/DOCX truth
- new report model
- new business logic

Those require PACK 06 V2.

---

# 24. FINAL ACCEPTANCE MATRIX

| Area | Required |
|------|:--------:|
| Architecture | ✅ |
| Runtime Pipeline | ✅ |
| Public API | ✅ |
| Data Model | ✅ |
| Template Engine | ✅ |
| Render Engine | ✅ |
| Export Engine | ✅ |
| Validation | ✅ |
| Testing | ✅ |
| PDF | ✅ |
| DOCX | ✅ |
| Manual QA | ✅ |
| Regression | ✅ |
| Product Owner Approval | ✅ |

Every row must be PASS.

---

# 25. FINAL DEFINITION OF DONE

PACK 06 is COMPLETE only when all of the following are true:

1. A frozen Date Selection result can be exported without recalculation.
2. PDF and DOCX originate from the same `DateSelectionReportModel`.
3. Customer-visible information is complete, accurate, and localized.
4. Recommendation order, compatible hours, and positive time slots exactly match the Date Selection Engine output.
5. All automated and manual acceptance criteria pass.
6. Product Owner signs off.

Only then may PACK 06 receive:

```text id="kwfjlwm"
STATUS

FINAL FREEZE

PASS
```

---

# 26. SUMMARY

The success criteria for PACK 06 can be expressed in one sentence:

> **A Date Selection result is calculated once, preserved without modification, rendered consistently, exported reliably, and delivered as a professional PDF or DOCX report suitable for commercial use.**

---

# STATUS

**READY FOR ARCHITECTURE FREEZE**