# PACK 06 — DATE SELECTION REPORT ENGINE

# 07_TEMPLATE_ENGINE.md

**Status:** DRAFT → CANONICAL REVIEW  
**Pack:** PACK 06  
**Module:** Date Selection Report Engine  
**Version:** 1.0

---

# 1. PURPOSE

This document defines the canonical Template Engine used by PACK 06.

The Template Engine is responsible for transforming a validated:

```text
DateSelectionReportModel
```

into a presentation template ready for rendering.

The Template Engine does **not**:

- calculate dates
- calculate Can Chi
- calculate Nạp Âm
- calculate Cung Phi
- calculate Hạ Nguyên
- calculate Đông/Tây Tứ Trạch
- calculate compatible hours
- calculate positive khắc
- reorder recommendations

The Template Engine is a presentation layer only.

---

# 2. POSITION IN THE PIPELINE

Canonical pipeline:

```text
SearchResult
      ↓
Report Adapter
      ↓
DateSelectionReportModel
      ↓
Template Engine
      ↓
Render Tree
      ↓
Render Engine
      ↓
PDF / DOCX
```

The Template Engine begins only after the ReportModel has passed validation.

---

# 3. TEMPLATE PRINCIPLES

## Principle 1

Templates never calculate.

---

## Principle 2

Templates never modify analytical truth.

---

## Principle 3

Templates are reusable.

The same template structure should serve:

- PDF
- DOCX

through different renderers.

---

## Principle 4

Templates are declarative.

They describe:

- layout
- placeholders
- grouping
- hierarchy

They never execute business rules.

---

## Principle 5

Templates are localization-safe.

No hardcoded English labels.

---

# 4. TEMPLATE ARCHITECTURE

Canonical hierarchy:

```text
Report Template
│
├── Header
├── Person
├── Search Period
├── Recommendation
├── Guidance
└── Footer
```

Every section is independently renderable.

---

# 5. ROOT TEMPLATE

Root template:

```text
date_selection_report
```

Contains:

```text
Header

↓

Person

↓

Search Period

↓

Recommendation List

↓

Guidance

↓

Footer
```

No analytical content appears outside these sections.

---

# 6. HEADER TEMPLATE

Purpose:

Display report identity.

Fields:

```text
Title

Subtitle

Generation Date

Report ID
```

Recommended title:

```text
BÁO CÁO CHỌN NGÀY TỐT
```

---

# 7. PERSON TEMPLATE

Input:

```text
PersonReportData
```

Fields:

```text
Họ và tên

Giới tính

Ngày sinh dương

Ngày sinh âm

Can Chi năm

Nạp Âm

Cung Phi

Nhóm Trạch
```

Presentation:

Compact information block.

---

# 8. SEARCH PERIOD TEMPLATE

Displays:

```text
Tháng tìm ngày tốt

09/2026

Số ngày đề xuất
```

Optional explanatory sentence:

```text
Các ngày dưới đây được lựa chọn theo dữ liệu cá nhân của bạn.
```

---

# 9. RECOMMENDATION TEMPLATE

Each recommendation uses one reusable template.

Structure:

```text
Recommendation

↓

Date Header

↓

Day Information

↓

Compatible Hours

↓

Positive Times
```

This template repeats for every recommended day.

---

# 10. DATE HEADER TEMPLATE

Displays:

```text
Ngày dương

↓

Ngày âm

↓

Kết quả ngày
```

Visual emphasis:

Date

↓

Result

↓

Lunar Date

---

# 11. DAY INFORMATION TEMPLATE

Fields:

```text
Can Chi năm

Can Chi tháng

Can Chi ngày

Nạp Âm

Cung Phi

Nhóm Trạch
```

Presentation rule:

```text
Cung Phi

Cấn (Thổ)
```

No separate Hành Cung row in report output.

Internally:

Cung

and

Cung Element

remain separate.

---

# 12. COMPATIBLE HOURS TEMPLATE

Displays:

```text
Giờ phù hợp Nhóm Trạch của bạn
```

Then:

```text
• Giờ Thìn (07:01–09:00) · Càn (Kim)

• Giờ Tỵ (09:01–11:00) · Khôn (Thổ)
```

One line per compatible hour.

No:

"Kết quả giờ"

---

# 13. POSITIVE TIMES TEMPLATE

Displays:

```text
Các thời điểm đẹp
```

Grouped:

```text
Đại An

•

•

•

Tốc Hỷ

•

•

•

Tiểu Cát

•

•
```

No negative classes.

---

# 14. GUIDANCE TEMPLATE

Displays short explanations:

```text
Đại An

...

Tốc Hỷ

...

Tiểu Cát

...
```

Purpose:

Customer education.

Not prediction.

---

# 15. FOOTER TEMPLATE

Contains:

```text
BTE Platform

Report Version

Page Number
```

Minimal.

---

# 16. PLACEHOLDER ENGINE

Templates contain placeholders only.

Examples:

```text
{{person.full_name}}

{{person.nayin}}

{{recommendation.day_result}}

{{recommendation.day_ganzhi}}

{{hour.branch}}
```

No calculations.

---

# 17. REPEATING BLOCKS

The following are repeatable:

Recommendations

Compatible Hours

Positive Times

Guidance Items

Every repeated block uses the same template instance.

---

# 18. CONDITIONAL BLOCKS

Allowed conditions:

Show Guidance only if configured.

Hide empty Positive Time groups.

Hide optional metadata.

Conditions may depend only on data presence.

Never on business logic.

---

# 19. EMPTY TEMPLATE STATES

If no recommendations:

Display:

```text
Không tìm thấy ngày phù hợp trong khoảng thời gian đã chọn.
```

Do not render empty recommendation sections.

---

# 20. LOCALIZATION

All labels come from localization resources.

Never hardcode:

Year Ganzhi

Month Ganzhi

etc.

Correct:

```text
Can Chi năm

Can Chi tháng

Can Chi ngày
```

---

# 21. TYPOGRAPHY TOKENS

Templates use semantic typography only.

Examples:

```text
Report Title

Section Title

Recommendation Date

Body

Caption
```

Actual fonts come from Theme Engine.

---

# 22. COLOR TOKENS

Templates request semantic colors:

```text
Primary

Accent

Element

Positive

Neutral
```

Theme Engine resolves actual colors.

---

# 23. ICON TOKENS

Optional semantic icons:

Calendar

Clock

Person

Report

Icons are optional.

Templates remain valid without icons.

---

# 24. PAGE BREAK HINTS

Recommendation block:

Preferred:

Keep together.

Avoid splitting:

Date Header

from

Day Information.

These are hints only.

Renderer decides final pagination.

---

# 25. TEMPLATE INVARIANTS

Templates must preserve:

Recommendation order.

Compatible Hour order.

Positive Time order.

No sorting.

No filtering.

---

# 26. TEMPLATE REUSE

The same recommendation template is reused for:

Recommendation 1

Recommendation 2

...

Recommendation N

Avoid duplicate templates.

---

# 27. PDF / DOCX SHARING

PDF

and

DOCX

share the same logical templates.

Only renderer-specific styling differs.

No duplicated analytical templates.

---

# 28. TEMPLATE VALIDATION

Before rendering:

Verify all required placeholders exist.

Missing mandatory placeholder:

Abort rendering.

Do not silently omit fields.

---

# 29. PERFORMANCE

Templates should be:

Compiled once.

Reused for repeated sections.

Avoid repeated parsing.

---

# 30. TEST STRATEGY

Verify:

Header template.

Person template.

Recommendation template.

Compatible hour template.

Positive time template.

Localization.

Empty state.

Placeholder coverage.

---

# 31. ACCEPTANCE

Template Engine PASS when:

✓ All sections render.

✓ Placeholders resolve.

✓ Recommendation template reusable.

✓ Compatible hours display correctly.

✓ Positive times grouped.

✓ Localization complete.

✓ No business logic exists inside templates.

---

# 32. SUMMARY

Canonical Template Engine:

```text
DateSelectionReportModel

↓

Templates

↓

Render Tree
```

Core rule:

> **Templates describe presentation only. They never calculate, reinterpret, or modify analytical truth.**

---

# STATUS

**READY FOR ARCHITECTURE REVIEW**