# PACK 06 — DATE SELECTION REPORT ENGINE

# 03_PUBLIC_API.md

**Status:** DRAFT → CANONICAL REVIEW  
**Pack:** PACK 06  
**Module:** Date Selection Report Engine  
**Version:** 1.0

---

# 1. PURPOSE

This document defines the canonical public API for PACK 06.

Its responsibility is to expose Date Selection report generation to the Customer Portal and future BTE clients.

This document does **not** define:

- report layout
- PDF rendering
- DOCX rendering
- report templates
- business rules
- Date Selection calculations

Those belong to other documents.

---

# 2. DESIGN PRINCIPLES

The public API follows six rules.

## Rule 1

Public API never performs Date Selection calculations.

It only consumes an already-generated canonical Date Selection result.

---

## Rule 2

Public API never recalculates:

- lunar date
- Can Chi
- Nạp Âm
- Cung Phi
- Hạ Nguyên
- Trạch
- compatible hours
- positive khắc

---

## Rule 3

PDF and DOCX share the same canonical ReportModel.

The API never exposes different analytical truth depending on export format.

---

## Rule 4

API must remain compatible with existing PACK 05 conventions wherever possible.

Do not invent a second reporting protocol.

---

## Rule 5

Every request must be deterministic.

The same SearchResult must always produce the same report.

---

## Rule 6

Public API is presentation-oriented.

Business logic belongs to Date Selection Engine.

---

# 3. API RESPONSIBILITIES

The API is responsible for:

✓ receiving export requests

✓ validating requests

✓ loading canonical SearchResult

✓ creating ReportModel

✓ invoking Report Engine

✓ returning PDF/DOCX

The API is NOT responsible for:

✗ analytical calculations

✗ ranking

✗ filtering

✗ interpretation

---

# 4. API ARCHITECTURE

Canonical runtime:

```text id="ydz9pd"
Portal

↓

Public API

↓

Report Adapter

↓

Report Model

↓

PACK 05 Report Runtime

↓

PDF / DOCX
```

---

# 5. API SURFACE

PACK 06 exposes one logical service:

```text id="9jlwm3"
Date Selection Report
```

Supported output formats:

- PDF
- DOCX

Future formats may include:

- HTML
- Markdown

These are outside V1.0.

---

# 6. CANONICAL ENDPOINTS

Preferred endpoints:

```text id="jlwm31"
POST /api/v1/date-selection/report/pdf

POST /api/v1/date-selection/report/docx
```

Alternative implementation:

```text id="jlwm32"
POST /api/v1/date-selection/report
```

with

```text id="jlwm33"
format

=

pdf

or

docx
```

The final implementation should follow the existing BTE reporting conventions.

Do not introduce parallel API styles.

---

# 7. REQUEST MODEL

Canonical request:

```text id="jlwm34"
DateSelectionReportRequest
```

Preferred fields:

```text id="jlwm35"
result_id

format
```

Reason:

Reuse the canonical SearchResult already stored by Date Selection.

Avoid transmitting large recommendation payloads again.

---

# 8. RESULT IDENTIFIER

Preferred flow:

```text id="jlwm36"
Search

↓

SearchResult

↓

ResultStore

↓

result_id

↓

Export
```

The report should be generated from the stored canonical result.

Do not rerun the search.

---

# 9. FORMAT ENUM

Allowed values:

```text id="jlwm37"
pdf

docx
```

Case-sensitive canonical values.

Reject unknown formats.

---

# 10. REQUEST VALIDATION

Required:

```text id="jlwm38"
result_id

format
```

Validation errors:

Missing result_id

↓

400

Missing format

↓

400

Unknown format

↓

400

Invalid result

↓

404

---

# 11. RESPONSE MODEL

Conceptual response:

```text id="jlwm39"
DateSelectionReportResponse
```

Fields:

```text id="jlwm3a"
report_id

format

filename

mime_type

generated_at
```

File delivery follows existing PACK 05 conventions.

---

# 12. FILE DELIVERY

Two acceptable implementations:

Option A

Binary response.

Option B

Temporary download URL.

Implementation should follow current BTE infrastructure.

Do not create a separate download system.

---

# 13. MIME TYPES

PDF

```text id="jlwm3b"
application/pdf
```

DOCX

```text id="jlwm3c"
application/vnd.openxmlformats-officedocument.wordprocessingml.document
```

---

# 14. FILE NAME

Recommended pattern:

```text id="jlwm3d"
bao-cao-chon-ngay-tot_<customer>_<MM-YYYY>.pdf
```

DOCX:

```text id="jlwm3e"
bao-cao-chon-ngay-tot_<customer>_<MM-YYYY>.docx
```

Use ASCII slug for filename only.

Report contents remain full Unicode.

---

# 15. REPORT SOURCE

Canonical source:

```text id="jlwm3f"
ResultStore

↓

SearchResult
```

The API must never reconstruct recommendations independently.

---

# 16. ADAPTER CONTRACT

Input:

```text id="jlwm3g"
SearchResult
```

Output:

```text id="jlwm3h"
DateSelectionReportModel
```

The adapter is the only translation layer.

The API does not manipulate report data.

---

# 17. SUCCESS FLOW

```text id="jlwm3i"
Client

↓

POST

↓

Validation

↓

Load SearchResult

↓

Report Adapter

↓

ReportModel

↓

Report Engine

↓

PDF

↓

Response
```

---

# 18. DOCX FLOW

Identical:

```text id="jlwm3j"
Client

↓

POST

↓

Validation

↓

Load SearchResult

↓

Report Adapter

↓

ReportModel

↓

DOCX Renderer

↓

Response
```

---

# 19. ERROR FLOW

Validation failure

↓

400

Missing SearchResult

↓

404

Renderer failure

↓

500

Export failure

↓

500

Errors must use the existing BTE API error structure.

---

# 20. ERROR MODEL

Recommended:

```text id="jlwm3k"
code

message

details

request_id
```

Follow current API error schema.

---

# 21. AUTHORIZATION

Use the same authorization model as existing Report Engine.

PACK 06 introduces no new authentication mechanism.

---

# 22. IDEMPOTENCY

The same:

```text id="jlwm3l"
result_id
```

must always generate the same analytical report.

Different timestamps in metadata are acceptable.

Analytical content must remain identical.

---

# 23. CACHE POLICY

Reports may be regenerated.

Do not cache analytical calculations separately.

If caching exists, cache rendered artifacts only.

---

# 24. RESULT CONSISTENCY

Mandatory invariant:

```text id="jlwm3m"
SearchResult

==

ReportModel

==

PDF

==

DOCX
```

No drift permitted.

---

# 25. PUBLIC CONTRACT

Customer-visible report fields:

```text id="jlwm3n"
Person

↓

Search Period

↓

Top Recommendations

↓

Compatible Hours

↓

Positive Time Slots

↓

Guidance
```

Do not expose:

- modulo arithmetic
- Tiểu Lục Nhâm implementation
- Hạ Nguyên algorithm
- internal ranking values

---

# 26. EXPORT BUTTONS

Portal actions:

```text id="jlwm3o"
Xuất PDF

Xuất DOCX
```

Buttons remain disabled until a valid SearchResult exists.

---

# 27. DOWNLOAD FLOW

```text id="jlwm3p"
Search

↓

Top-5

↓

Export

↓

Download
```

No additional confirmation screens.

---

# 28. LOGGING

Recommended:

```text id="jlwm3q"
Report Requested

↓

Validation Passed

↓

Rendered

↓

Delivered
```

Include:

- report_id
- format
- duration

Avoid logging unnecessary personal data.

---

# 29. API VERSIONING

Current:

```text id="jlwm3r"
v1
```

Future incompatible changes require:

```text id="jlwm3s"
v2
```

Do not silently alter response semantics.

---

# 30. ACCEPTANCE

Public API is PASS when:

✓ accepts valid result_id

✓ validates request

✓ loads canonical SearchResult

✓ generates ReportModel

✓ renders PDF

✓ renders DOCX

✓ preserves analytical truth

✓ returns downloadable file

✓ follows existing BTE API conventions

---

# 31. SUMMARY

PACK 06 exposes a minimal public API.

The API never calculates.

It only transforms:

```text id="jlwm3t"
Frozen SearchResult

↓

ReportModel

↓

PDF / DOCX
```

Core principle:

> **One analytical result. One report model. Multiple export formats.**

---

# STATUS

**READY FOR ARCHITECTURE REVIEW**