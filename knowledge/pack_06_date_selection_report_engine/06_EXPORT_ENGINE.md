# PACK 06 — DATE SELECTION REPORT ENGINE

# 06_EXPORT_ENGINE.md

**Status:** DRAFT → CANONICAL REVIEW  
**Pack:** PACK 06  
**Module:** Date Selection Report Engine  
**Version:** 1.0

---

# 1. PURPOSE

This document defines the canonical Export Engine for PACK 06.

The Export Engine is responsible for converting a fully rendered report into downloadable customer files.

It does **not**:

- calculate analytical results
- modify report content
- perform rendering
- interpret Date Selection data

Its only responsibility is:

> **Convert one Render Tree into one export artifact.**

---

# 2. POSITION IN THE ARCHITECTURE

Canonical pipeline:

```text id="f0ps92"
Date Selection Engine
        ↓
SearchResult
        ↓
Report Adapter
        ↓
Report Model
        ↓
Render Engine
        ↓
Render Tree
        ↓
Export Engine
        ↓
PDF / DOCX
```

Export begins **only after** rendering is complete.

---

# 3. EXPORT PRINCIPLES

## Principle 1

Export never changes analytical truth.

---

## Principle 2

Export never changes layout decisions.

---

## Principle 3

Export never recalculates anything.

---

## Principle 4

PDF and DOCX export from the same Render Tree.

---

## Principle 5

One render.

Many export formats.

---

# 4. EXPORT INPUT

Canonical input:

```text id="bb90mv"
RenderTree
```

RenderTree is immutable.

Export Engine receives a read-only object.

---

# 5. EXPORT OUTPUT

Supported formats in V1.0:

```text id="1gwsx8"
PDF

DOCX
```

Future formats:

- HTML
- Markdown
- ODT

Not part of V1.0.

---

# 6. EXPORT FLOW

Canonical flow:

```text id="cmo32q"
RenderTree
      ↓
Export Dispatcher
      ↓
Format Resolver
      ↓
Exporter
      ↓
Binary File
      ↓
Delivery
```

---

# 7. EXPORT DISPATCHER

Component:

```text id="4k6t1l"
ExportDispatcher
```

Responsibilities:

- determine format
- select exporter
- invoke exporter

It performs no rendering.

---

# 8. FORMAT RESOLUTION

Supported values:

```text id="2kwf4q"
pdf

docx
```

Unknown format:

Return validation error.

Do not silently substitute another exporter.

---

# 9. PDF EXPORTER

Canonical exporter:

```text id="s6v98z"
PdfExporter
```

Consumes:

```text id="e4sy6v"
RenderTree
```

Produces:

```text id="6ffy2v"
PDF Binary
```

Responsibilities:

- page composition
- typography
- pagination
- image embedding
- Unicode rendering

No analytical logic.

---

# 10. DOCX EXPORTER

Canonical exporter:

```text id="s9ewu7"
DocxExporter
```

Consumes:

```text id="xto94w"
RenderTree
```

Produces:

```text id="2r5z5r"
DOCX Binary
```

Responsibilities:

- editable document
- styles
- headings
- tables
- paragraph flow

No analytical logic.

---

# 11. EXPORT CONTRACT

Every exporter guarantees:

```text id="dd1j5y"
Input

RenderTree

↓

Output

One document
```

No exporter may request additional analytical data.

---

# 12. FILE NAMING

Canonical filename:

PDF

```text id="2w9m7m"
bao-cao-chon-ngay-tot_<customer>_<MM-YYYY>.pdf
```

DOCX

```text id="8ew2ts"
bao-cao-chon-ngay-tot_<customer>_<MM-YYYY>.docx
```

Examples:

```text id="uzh9yx"
bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.pdf
```

```text id="b4saz5"
bao-cao-chon-ngay-tot_nguyen-tien-son_09-2026.docx
```

Filename:

ASCII only.

Document contents:

Full Unicode.

---

# 13. FILE METADATA

Suggested metadata:

```text id="6cfd0f"
Title

Báo cáo Chọn ngày tốt

Author

BTE Platform

Subject

Date Selection Report

Keywords

BTE
Ngày tốt
Date Selection
```

Metadata never changes analytical content.

---

# 14. PDF REQUIREMENTS

The PDF must:

✓ preserve Vietnamese Unicode

✓ preserve typography

✓ preserve page order

✓ preserve recommendation order

✓ print correctly

✓ embed fonts where required

---

# 15. DOCX REQUIREMENTS

The DOCX must:

✓ remain editable

✓ preserve headings

✓ preserve recommendation order

✓ preserve Unicode

✓ preserve semantic sections

---

# 16. EXPORT CONSISTENCY

Mandatory invariant:

```text id="5v1n4l"
RenderTree

↓

PDF

↓

Same analytical truth
```

```text id="l4x0kv"
RenderTree

↓

DOCX

↓

Same analytical truth
```

Formatting may differ.

Content may not.

---

# 17. DELIVERY

Supported delivery:

Download.

Browser save.

Temporary file response.

Follow existing PACK 05 delivery mechanism.

---

# 18. EXPORT ERRORS

Possible failures:

Unknown format

↓

400

Renderer output missing

↓

500

Exporter failure

↓

500

Filesystem failure

↓

500

Each error must produce structured diagnostics.

---

# 19. TEMP FILE POLICY

Temporary artifacts:

- unique filename
- isolated workspace
- cleanup after completion when appropriate

Avoid overwriting existing exports.

---

# 20. CONCURRENCY

Multiple export requests:

Must be independent.

No shared mutable export state.

Unique report identifiers.

---

# 21. LOGGING

Log:

```text id="jlwm62"
Export Requested

↓

Format

↓

Filename

↓

Duration

↓

Success
```

Do not log private report contents.

---

# 22. PERFORMANCE

Export should:

Reuse RenderTree.

Avoid rebuilding ReportModel.

Avoid rerendering.

Export should be O(1) relative to analytical work.

---

# 23. RESOURCE MANAGEMENT

Exporters must:

Release:

- streams
- temporary objects
- file handles

No leaked resources.

---

# 24. PDF PAGINATION

Exporter respects pagination hints from Render Engine.

Exporter may:

Move entire recommendation block.

Exporter may not:

Split analytical fields incorrectly.

---

# 25. DOCX STYLING

Use reusable paragraph styles.

Examples:

```text id="jlwm63"
Heading

Section

Recommendation

Body

Caption
```

Do not apply direct formatting everywhere.

---

# 26. EXPORT VALIDATION

Before writing output:

Verify:

- RenderTree exists
- mandatory sections exist
- recommendation blocks exist
- metadata exists

Abort if invalid.

---

# 27. DIGITAL CONSISTENCY

Two exports generated from the same RenderTree should contain identical:

- recommendations
- hours
- positive times
- customer information

Only presentation differs.

---

# 28. EXPORT SECURITY

Never expose:

Internal paths.

Temporary filesystem locations.

Stack traces.

Analytical internals.

Return user-friendly errors.

---

# 29. FUTURE EXTENSIBILITY

Future exporters may include:

- HTML
- Markdown
- ODT
- ePub

They must implement the same export contract.

---

# 30. EXPORT INTERFACE

Conceptually:

```text id="jlwm64"
Exporter

export(RenderTree)

↓

Binary Artifact
```

Every exporter follows the same interface.

---

# 31. TEST STRATEGY

Verify:

PDF export.

DOCX export.

Unicode.

Long names.

Multiple recommendations.

Large reports.

Filename generation.

Repeated exports.

---

# 32. REGRESSION TESTS

Confirm:

No analytical value changes during export.

Recommendation order preserved.

Compatible hours preserved.

Positive times preserved.

---

# 33. ACCEPTANCE

Export Engine PASS when:

✓ PDF exports successfully.

✓ DOCX exports successfully.

✓ Unicode preserved.

✓ Recommendation order preserved.

✓ File naming correct.

✓ Delivery succeeds.

✓ Same RenderTree generates equivalent PDF/DOCX content.

✓ No analytical mutation.

---

# 34. SUMMARY

Canonical Export Engine:

```text id="jlwm65"
RenderTree
      ↓
Export Dispatcher
      ↓
PdfExporter
DocxExporter
      ↓
Binary File
      ↓
Download
```

Core rule:

> **Export exactly what was rendered. Never reinterpret analytical truth.**

---

# STATUS

**READY FOR ARCHITECTURE REVIEW**