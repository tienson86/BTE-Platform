# PACK 06 — DATE SELECTION REPORT ENGINE

# 02_RUNTIME_PIPELINE.md

**Status:** DRAFT → CANONICAL REVIEW  
**Pack:** PACK 06  
**Module:** Date Selection Report Engine  
**Version:** 1.0

---

# 1. PURPOSE

This document defines the canonical runtime pipeline for PACK 06.

Its responsibility is to describe how a completed Date Selection result becomes an exportable report.

This document does **not** describe:

- report layout
- PDF rendering
- DOCX rendering
- template design
- UI

Those are covered by later documents.

This document only defines:

> **Runtime data flow**

---

# 2. DESIGN PRINCIPLES

The runtime follows five fundamental rules.

## Rule 1

Date Selection Engine is the only analytical engine.

PACK 06 never recalculates:

- lunar calendar
- Ganzhi
- Nạp Âm
- Cung Phi
- Hạ Nguyên
- compatible hours
- positive khắc
- Top-5 ranking

---

## Rule 2

PACK 06 is read-only.

Input:

```text id="fxtmbn"
Canonical DateSelectionSearchResult
```

Output:

```text id="jjlwmq"
PDF

DOCX
```

---

## Rule 3

Every export uses exactly the same canonical report model.

```text id="jkpjlwm"
SearchResult

↓

ReportModel

↓

PDF

DOCX
```

---

## Rule 4

No renderer owns business logic.

Renderers consume data only.

---

## Rule 5

One runtime.

One truth.

Many output formats.

---

# 3. HIGH LEVEL PIPELINE

Canonical runtime:

```text id="iq5r0d"
User

↓

/choose-date

↓

Date Selection Engine

↓

Canonical SearchResult

↓

PACK 06 Adapter

↓

DateSelectionReportModel

↓

Validation

↓

Template

↓

Renderer

↓

Exporter

↓

PDF / DOCX

↓

Download
```

Every stage has exactly one responsibility.

---

# 4. STAGE 01 — USER ACTION

Entry point:

```text id="k3cxxw"
/choose-date
```

The user performs:

- Search
- Receives Top-5
- Reviews results

At this point:

No report exists.

---

# 5. STAGE 02 — SEARCH RESULT

Date Selection Engine returns:

```text id="7eb8p0"
DateSelectionSearchResult
```

This object is frozen.

PACK 06 must never modify it.

---

# 6. STAGE 03 — EXPORT REQUEST

The user clicks:

```text id="s1r7j8"
Xuất PDF
```

or

```text id="jx4pzm"
Xuất DOCX
```

Only then does PACK 06 start.

No background report generation.

---

# 7. STAGE 04 — REPORT REQUEST

Conceptual request:

```text id="bpjlwm"
DateSelectionReportRequest
```

Contains:

```text id="wjlwmq"
search_result

format
```

or

```text id="wjlwmr"
search_result_id

format
```

depending on the existing ResultStore architecture.

Implementation must follow current repository conventions.

---

# 8. STAGE 05 — REPORT ADAPTER

Component:

```text id="mjlwmq"
DateSelectionReportAdapter
```

Input:

```text id="jjlwmr"
DateSelectionSearchResult
```

Output:

```text id="8jlwmq"
DateSelectionReportModel
```

Responsibilities:

✓ Validate

✓ Normalize

✓ Prepare presentation model

Forbidden:

✗ Calculate

✗ Rerank

✗ Reinterpret

---

# 9. ADAPTER PIPELINE

Canonical flow:

```text id="jlwmqa"
SearchResult

↓

Structural Validation

↓

Semantic Validation

↓

Presentation Normalization

↓

Report Model
```

---

# 10. STAGE 06 — STRUCTURAL VALIDATION

Verify required objects exist.

Required:

```text id="jlwmqb"
Person

Recommendations

Compatible Hours

Positive Khắc
```

Missing mandatory objects stop report generation.

---

# 11. STAGE 07 — SEMANTIC VALIDATION

Verify analytical consistency.

Examples:

```text id="jlwmqc"
Person Trạch

==

Recommendation Trạch
```

```text id="jlwmqd"
Recommendation order

matches

SearchResult order
```

```text id="jlwmqe"
Positive Khắc

contain

only approved values
```

---

# 12. STAGE 08 — PRESENTATION NORMALIZATION

This stage may perform presentation-only transformations.

Allowed:

Example:

```text id="jlwmqf"
Cung

Cấn

+

Thổ

↓

Cấn (Thổ)
```

Allowed:

Vietnamese date formatting

Grouping positive khắc

Display labels

Forbidden:

Changing analytical values.

---

# 13. STAGE 09 — REPORT MODEL

Output:

```text id="jlwmqg"
DateSelectionReportModel
```

After this point:

The analytical pipeline is finished.

Everything downstream is rendering.

---

# 14. STAGE 10 — REPORT VALIDATOR

Validate final report object.

Checks:

Person block

↓

Recommendation block

↓

Compatible hours

↓

Positive time slots

↓

Metadata

↓

Version

No renderer may start before validation succeeds.

---

# 15. STAGE 11 — TEMPLATE RESOLUTION

Determine template.

Example:

```text id="jlwmqh"
date_selection_report.html
```

or

```text id="jlwmqi"
date_selection_report.docx
```

No analytical decisions occur here.

---

# 16. STAGE 12 — LAYOUT COMPOSITION

Construct report sections.

Example:

```text id="jlwmqj"
Header

↓

Person

↓

Search Period

↓

Recommendation 1

↓

Recommendation 2

↓

...

↓

Guidance

↓

Footer
```

Only presentation.

---

# 17. STAGE 13 — RENDER

Renderer receives:

```text id="jlwmqk"
DateSelectionReportModel
```

Produces:

Internal render tree.

No calculations.

---

# 18. STAGE 14 — EXPORT

Export target:

PDF

or

DOCX

Exporter uses existing PACK 05 infrastructure.

Do not duplicate exporters.

---

# 19. STAGE 15 — DELIVERY

Output:

```text id="jlwmql"
Download

Save

Open
```

Delivery follows current BTE conventions.

---

# 20. FAILURE PIPELINE

If validation fails:

```text id="jlwmqm"
SearchResult

↓

Validation Error

↓

Abort

↓

User-friendly message
```

Never export partially valid reports.

---

# 21. RUNTIME OWNERSHIP

| Stage | Owner |
|--------|-------|
| Search | Date Selection Engine |
| SearchResult | Date Selection Engine |
| Report Adapter | PACK 06 |
| Report Model | PACK 06 |
| Validator | PACK 06 |
| Template | PACK 05 |
| Renderer | PACK 05 |
| Export | PACK 05 |

Ownership must never overlap.

---

# 22. RESULTSTORE INTEGRATION

PACK 06 should integrate with the existing BTE ResultStore.

Preferred flow:

```text id="jlwmqn"
Search

↓

ResultStore

↓

Current SearchResult

↓

Export
```

Do not rerun the search simply to export.

The exported report must reflect exactly what the user reviewed.

---

# 23. PDF / DOCX CONSISTENCY

Canonical invariant:

```text id="jlwmqo"
ReportModel

↓

PDF

DOCX
```

Both outputs must contain identical analytical facts.

Formatting may differ.

Truth may not.

---

# 24. PERFORMANCE

Runtime should perform:

One adapter pass

↓

One validation pass

↓

One render

↓

One export

Avoid unnecessary object duplication.

---

# 25. LOGGING

Recommended log sequence:

```text id="jlwmqp"
Export Requested

↓

Adapter Started

↓

Validation Passed

↓

Render Started

↓

Export Finished

↓

Delivered
```

Include:

- report id
- duration
- format

Do not log unnecessary personal data.

---

# 26. ERROR HANDLING

Possible failures:

Missing SearchResult

↓

Invalid Recommendation

↓

Template Missing

↓

Renderer Failure

↓

Export Failure

Each failure must produce a clear user-visible message and structured log entry.

---

# 27. SEQUENCE DIAGRAM

Canonical sequence:

```text id="jlwmqq"
User
 │
 │ Export
 ▼
Portal
 │
 ▼
Date Selection Result
 │
 ▼
Report Adapter
 │
 ▼
Validator
 │
 ▼
Report Model
 │
 ▼
Template Engine
 │
 ▼
Render Engine
 │
 ▼
PDF / DOCX Export
 │
 ▼
Download
```

---

# 28. RUNTIME INVARIANTS

The following must always remain true.

```text id="’winiwr"
SearchResult

==

ReportModel Truth
```

```text id="qbbv7m"
ReportModel

==

PDF Truth
```

```text id="r7e6l1"
ReportModel

==

DOCX Truth
```

No analytical drift.

---

# 29. ACCEPTANCE PIPELINE

PACK 06 runtime is PASS only if:

✓ SearchResult is reused.

✓ No recalculation occurs.

✓ Validation succeeds.

✓ ReportModel created.

✓ PDF generated.

✓ DOCX generated.

✓ Download succeeds.

✓ Analytical truth preserved.

---

# 30. PIPELINE SUMMARY

The canonical runtime is:

```text id="m2wdr5"
Date Selection Engine
        ↓
Frozen SearchResult
        ↓
DateSelectionReportAdapter
        ↓
DateSelectionReportModel
        ↓
Validation
        ↓
Template Resolution
        ↓
Layout Composition
        ↓
Render
        ↓
Export
        ↓
PDF / DOCX
        ↓
Download
```

This runtime is immutable.

Every future enhancement must plug into this pipeline rather than bypass it.

---

# STATUS

**READY FOR ARCHITECTURE REVIEW**