# PACK 06 — DATE SELECTION REPORT ENGINE

# 05_RENDER_ENGINE.md

**Status:** DRAFT → CANONICAL REVIEW  
**Pack:** PACK 06  
**Module:** Date Selection Report Engine  
**Version:** 1.0

---

# 1. PURPOSE

This document defines the canonical Render Engine for PACK 06.

Its responsibility is to transform a validated:

```text id="0cb0ef"
DateSelectionReportModel
```

into a presentation-ready render tree.

The Render Engine does **not**:

- calculate dates
- calculate Can Chi
- calculate Nạp Âm
- calculate Cung Phi
- calculate Hạ Nguyên
- calculate Trạch
- rank recommendations
- generate analytical results

Those responsibilities belong exclusively to Date Selection Engine.

---

# 2. DESIGN PRINCIPLES

The Render Engine follows seven immutable principles.

---

## Principle 1

Render only.

Never calculate.

---

## Principle 2

Every renderer consumes exactly the same:

```text id="skc7hp"
DateSelectionReportModel
```

No renderer-specific analytical objects.

---

## Principle 3

Rendering must be deterministic.

The same ReportModel must always produce the same visual structure.

---

## Principle 4

PDF and DOCX must render from identical analytical truth.

Only typography and layout may differ.

---

## Principle 5

Rendering never mutates the report model.

Renderers are read-only.

---

## Principle 6

Presentation belongs here.

Business logic never belongs here.

---

## Principle 7

Rendering is modular.

Each report section renders independently.

---

# 3. RENDER PIPELINE

Canonical flow:

```text id="rh0z4e"
DateSelectionReportModel

↓

Render Context

↓

Section Renderers

↓

Render Tree

↓

PDF Renderer

DOCX Renderer
```

---

# 4. RENDER CONTEXT

Before rendering begins:

Create:

```text id="t4ql2q"
DateSelectionRenderContext
```

Contains:

```text id="vj7w8b"
metadata

theme

locale

page

layout

report
```

No analytical values are modified.

---

# 5. SECTION RENDERERS

The report is rendered section-by-section.

Canonical render order:

```text id="bjz7sx"
Header

↓

Person

↓

Search Period

↓

Recommendation Blocks

↓

Guidance

↓

Footer
```

Each renderer is independent.

---

# 6. HEADER RENDERER

Input:

```text id="i0k5tm"
metadata
```

Produces:

```text id="pyw8uv"
Title

Subtitle

Generation Date

Page Header
```

No analytical content.

---

# 7. PERSON RENDERER

Input:

```text id="lt1c0f"
PersonReportData
```

Produces:

```text id="0ocnch"
Họ và tên

Giới tính

Ngày sinh dương

Ngày sinh âm

Can Chi năm

Nạp Âm

Cung Phi

Nhóm Trạch
```

Recommended presentation:

```text id="a4e17m"
Cung Phi

Khôn (Thổ)
```

Presentation only.

---

# 8. SEARCH PERIOD RENDERER

Input:

```text id="y2qj6n"
SearchPeriodReportData
```

Produces:

```text id="ex6l6r"
Tháng tìm ngày tốt

09/2026
```

Optional:

Số ngày đề xuất.

---

# 9. RECOMMENDATION RENDERER

The largest renderer.

Input:

```text id="jlwm5a"
RecommendedDateReportData
```

Produces:

```text id="jlwm5b"
Date Header

↓

Day Information

↓

Compatible Hours

↓

Positive Times
```

One recommendation block.

---

# 10. DATE HEADER

Visual hierarchy:

```text id="jlwm5c"
04/09/2026

23/07/2026 âm

ĐẠI AN
```

Date largest.

Result second.

Lunar date secondary.

---

# 11. DAY INFORMATION RENDERER

Fields:

```text id="jlwm5d"
Can Chi năm

Can Chi tháng

Can Chi ngày

Nạp Âm

Cung Phi

Nhóm Trạch
```

Presentation:

Compact.

Readable.

No duplicated labels.

---

# 12. COMPATIBLE HOUR RENDERER

Input:

```text id="jlwm5e"
compatible_hours[]
```

Produces:

```text id="jlwm5f"
Giờ phù hợp Nhóm Trạch của bạn

↓

Hour rows
```

Each row:

```text id="jlwm5g"
Giờ Thìn

(07:01–09:00)

Càn (Kim)
```

No six-state result.

No "Kết quả giờ".

---

# 13. HOUR ROW RENDERER

Each compatible hour renders:

```text id="jlwm5h"
Hour Branch

↓

Time Range

↓

Cung (Element)
```

Example:

```text id="jlwm5i"
Giờ Thân

15:01–17:00

Khôn (Thổ)
```

Compact.

One row.

---

# 14. POSITIVE TIME RENDERER

Input:

```text id="jlwm5j"
positive_ke[]
```

Produces grouped output.

Example:

```text id="jlwm5k"
Đại An

...

Tốc Hỷ

...

Tiểu Cát
```

Grouping order:

1.

Đại An

2.

Tốc Hỷ

3.

Tiểu Cát

Never reorder.

---

# 15. GUIDANCE RENDERER

Input:

```text id="jlwm5l"
GuidanceData
```

Produces:

```text id="jlwm5m"
Đại An

...

Tốc Hỷ

...

Tiểu Cát
```

Short educational text only.

---

# 16. FOOTER RENDERER

Contains:

```text id="jlwm5n"
BTE Platform

Report Version

Page Number
```

Minimal.

---

# 17. RENDER TREE

The Render Engine builds:

```text id="jlwm5o"
Render Tree

Header

Person

Search

Recommendation

Guidance

Footer
```

No exporter-specific nodes.

---

# 18. PAGE COMPOSITION

Renderer composes semantic blocks.

Exporter decides actual pagination.

Renderer should only suggest:

Keep recommendation together.

Avoid splitting.

---

# 19. PAGINATION HINTS

Recommendation block:

Preferred:

Stay on one page.

If impossible:

Split only between:

Compatible Hours

and

Guidance.

Never split:

Date Header

from

Day Information.

---

# 20. TYPOGRAPHY TOKENS

Renderer uses semantic typography.

Examples:

```text id="jlwm5p"
Title

Section Title

Recommendation Date

Result

Body

Caption
```

No hardcoded font sizes.

Theme controls actual sizes.

---

# 21. COLOR TOKENS

Renderer requests semantic colors only.

Example:

```text id="jlwm5q"
Primary

Accent

Positive

Neutral

Element
```

Renderer never specifies RGB values.

Theme resolves colors.

---

# 22. BADGE TOKENS

Renderer may request:

```text id="jlwm5r"
Element Badge

Result Badge

Section Badge
```

Theme defines appearance.

---

# 23. ICON TOKENS

Renderer references semantic icons only.

Example:

```text id="jlwm5s"
Calendar

Clock

Person
```

No embedded icon graphics.

---

# 24. LOCALIZATION

Renderer requests localized labels.

Never embed English labels.

Example:

```text id="jlwm5t"
Can Chi năm

not

Year Ganzhi
```

Localization comes from resource bundles.

---

# 25. EMPTY STATES

No recommendations:

Render:

```text id="jlwm5u"
Không tìm thấy ngày phù hợp.
```

No empty tables.

---

# 26. OVERFLOW POLICY

Long names:

Wrap naturally.

Do not overflow page.

Compatible hours:

Wrap to next line if required.

---

# 27. PRINT SAFETY

Renderer must produce:

- monochrome-safe output
- grayscale-safe output

Never depend solely on color.

---

# 28. RENDER INVARIANTS

Renderer must preserve:

Recommendation order.

Compatible hour order.

Positive khắc order.

No sorting.

No filtering.

---

# 29. PERFORMANCE

Each section renders once.

Avoid duplicate render passes.

Avoid duplicate object traversal.

---

# 30. ERROR HANDLING

Renderer failures:

Section renderer

↓

Abort rendering

↓

Return structured error

Do not silently omit sections.

---

# 31. RENDER CONTRACT

Input:

```text id="jlwm5v"
DateSelectionReportModel
```

Output:

```text id="jlwm5w"
Render Tree
```

Nothing else.

---

# 32. PDF RENDERER

Consumes:

```text id="jlwm5x"
Render Tree
```

Produces:

PDF.

No analytical logic.

---

# 33. DOCX RENDERER

Consumes:

```text id="jlwm5y"
Render Tree
```

Produces:

DOCX.

No analytical logic.

---

# 34. RENDER CONSISTENCY

Mandatory:

```text id="jlwm5z"
Render Tree

↓

PDF

↓

Same analytical content
```

```text id="jlwm60"
Render Tree

↓

DOCX

↓

Same analytical content
```

---

# 35. TEST STRATEGY

Verify:

Every renderer.

Every section.

Every recommendation.

Empty state.

Long names.

Unicode.

Vietnamese labels.

Recommendation grouping.

---

# 36. ACCEPTANCE

Render Engine PASS when:

✓ RenderContext created

✓ All sections rendered

✓ Recommendation blocks correct

✓ Compatible hours rendered

✓ Positive times grouped

✓ Guidance rendered

✓ Footer rendered

✓ No analytical mutation

✓ PDF renderer succeeds

✓ DOCX renderer succeeds

---

# 37. SUMMARY

The Render Engine is a presentation pipeline only.

Canonical flow:

```text id="jlwm61"
ReportModel

↓

Render Context

↓

Section Renderers

↓

Render Tree

↓

PDF

DOCX
```

Core rule:

> **Render faithfully. Never reinterpret analytical truth.**

---

# STATUS

**READY FOR ARCHITECTURE REVIEW**