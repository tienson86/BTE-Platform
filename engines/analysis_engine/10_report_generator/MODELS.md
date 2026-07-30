# Report Generator Domain Models

**Module:** `engines/analysis_engine/10_report_generator`  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the official domain model specification for the Report Generator.

---

# 2. Design Principles

- Immutable by default
- Explicit ownership
- Strong typing
- Deterministic serialization
- Version compatibility
- Non-destructive assembly
- Format-neutral canonical model

---

# 3. Domain Model Overview

```text
ReportAssemblyContext (Input)
        │
        │  reads InterpretationResult
        │  reads AnalysisResult (optional)
        ▼
ReportAssemblyEvaluationContext
        │
        ▼
StructuredReport
        │
        ├── ReportSection[]
        ├── StructuredDataBlock[]
        ├── ReportMetadata
        └── FormatHints
        │
        ▼
HtmlReportArtifact
PdfReportArtifact
JsonReportArtifact
MarkdownReportArtifact
        │
        ▼
ReportGeneratorResult
```

No dedicated ReportGeneratorInput wrapper is defined beyond ReportAssemblyContext.

---

# 4. ReportAssemblyContext (External)

Owner: Analysis Runtime / Orchestrator

Provides:

- `interpretation_result` — mandatory
- `analysis_result` — optional; required when format profile declares structured analytical sections
- `format_profile` — requested formats and layout policy
- request / trace identifiers as defined by runtime contracts

Mutability: immutable input for the stage.

---

# 5. Upstream Result Models (External)

| Model | Owner | Usage |
|-------|-------|-------|
| InterpretationResult | Interpretation Engine | Primary narrative and section source |
| AnalysisResult | Analysis Runtime | Read-only structured data binding |

Report Generator must not redefine or mutate these models.

---

# 6. ReportAssemblyEvaluationContext

Request-scoped internal working context. Not part of public API.

---

# 7. StructuredReport

Canonical internal assembly model and primary structured output.

Shall include at minimum:

- report identity / version metadata
- ordered report sections
- structured analytical data blocks (when bound)
- source trace references to InterpretationResult and AnalysisResult
- format-neutral content tree suitable for multi-format serialization

StructuredReport is the single source of truth for all format outputs.

---

# 8. ReportSection

Presentation section bound from InterpretationResult content.

Fields include section identity, title, body content reference, ordering, and trace metadata.

Report Generator does not generate section text; it binds published interpretation content.

---

# 9. StructuredDataBlock

Read-only analytical data section bound from AnalysisResult.

Used for tables, charts, structured summaries, and API-oriented payloads.

No recomputation or reinterpretation occurs during binding.

---

# 10. Format Artifacts

| Model | Description |
|-------|-------------|
| HtmlReportArtifact | HTML document output |
| PdfReportArtifact | PDF document output |
| JsonReportArtifact | JSON-serializable report envelope |
| MarkdownReportArtifact | Markdown document output |

All artifacts derive deterministically from StructuredReport.

---

# 11. ReportGeneratorResult

Public immutable output model.

Shall include at minimum:

- `structured_report`
- `html`
- `pdf`
- `json`
- `markdown`
- diagnostics / execution metadata slots aligned with shared runtime models

Exact field-level schema remains backward compatible within V1.x once published.

---

# 12. Format Profile

Declares requested output formats, layout policy, and whether AnalysisResult structured binding is mandatory.

Owned by runtime/orchestrator; consumed read-only by Report Generator.

---

# 13. Ownership

All Report Generator-specific models above are owned by Report Generator unless marked external.

---

# 14. Acceptance Criteria

Domain models are accepted when overview, StructuredReport contract, format artifacts, and ReportGeneratorResult contract are complete.
