# Report Generator Execution Flow

**Module:** `engines/analysis_engine/10_report_generator`  
**Version:** V1.0.0  
**Status:** Frozen (Execution Flow Specification)

---

# 1. Purpose

This document defines the end-to-end execution flow of the Report Generator.

---

# 2. Execution Principles

- Deterministic
- Stateless
- Non-mutating
- Immutable
- Assembly-only
- Fail-fast / fail-closed

---

# 3. High-Level Flow

```text
Receive ReportAssemblyContext
        │
        ▼
Validate Context
        │
        ▼
Read InterpretationResult
        │
        ▼
Read AnalysisResult (if required by profile)
        │
        ▼
Validate Assembly Prerequisites
        │
        ▼
Resolve Format Profile
        │
        ▼
Build StructuredReport
        │
        ▼
Bind Interpreted Sections
        │
        ▼
Bind Structured Analytical Data
        │
        ▼
Validate StructuredReport Schema
        │
        ▼
Serialize HTML
        │
        ▼
Serialize PDF
        │
        ▼
Serialize JSON
        │
        ▼
Serialize Markdown
        │
        ▼
Build Immutable ReportGeneratorResult
        │
        ▼
Publish ReportGeneratorResult
```

---

# 4. Stage Definitions

## Stage 1 — Receive ReportAssemblyContext

Accept shared immutable ReportAssemblyContext from Analysis Runtime or orchestrator.

## Stage 2 — Validate Context

Validate integrity, format profile, and pipeline readiness for report assembly.

## Stage 3 — Read Upstream Results

Read published InterpretationResult and, when required, AnalysisResult from context.

## Stage 4 — Validate Assembly Prerequisites

Verify mandatory interpreted sections and required structured data slots are present.

## Stage 5 — Resolve Format Profile

Determine requested output formats and layout rules from format profile.

## Stage 6 — Build StructuredReport

Construct canonical internal report model from bound inputs.

## Stage 7 — Section Binding

Map InterpretationResult sections into StructuredReport layout slots without altering interpretation semantics.

## Stage 8 — Data Binding

Attach read-only analytical data from AnalysisResult where profile requires structured sections.

## Stage 9 — Format Serialization

Derive HTML, PDF, JSON, and Markdown from StructuredReport using deterministic serializers.

## Stage 10 — Build and Publish Result

Construct immutable `ReportGeneratorResult` and return to orchestrator.

---

# 5. Assembly Order

Section binding follows InterpretationResult section order as published.

Structured data binding follows AnalysisResult canonical stage order when present:

```text
Strength → Temperature → Pattern → Useful God → Ten Gods → Combination → ShenSha → Luck → Summary
```

Binding reflects presentation order; it does not re-execute analysis.

---

# 6. Data Movement

```text
ReportAssemblyContext + InterpretationResult [+ AnalysisResult]
        │
        ▼
Internal assembly intermediates (request-scoped)
        │
        ▼
StructuredReport (canonical)
        │
        ▼
Format artifacts (HTML / PDF / JSON / Markdown)
        │
        ▼
ReportGeneratorResult (immutable)
```

---

# 7. Failure Points

Any stage may fail closed with classified errors.

Incomplete interpretation or missing mandatory format outputs must not produce ReportGeneratorResult.

---

# 8. Acceptance Criteria

Execution flow is accepted when order, assembly semantics, serialization rules, and publish rules are complete.
