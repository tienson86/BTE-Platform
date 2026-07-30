# Report Generator Architecture

**Module:** `engines/analysis_engine/10_report_generator`  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the official software architecture of the Report Generator.

---

# 2. Architectural Goals

- Provide deterministic multi-format report assembly.
- Isolate presentation assembly from interpretation logic.
- Preserve upstream semantic integrity of AnalysisResult and InterpretationResult.
- Produce reusable `ReportGeneratorResult` for Delivery Layer consumption.
- Guarantee reproducible assembly results for identical inputs and format profiles.
- Complete the Analysis Engine output publication pipeline.

---

# 3. Position in the BTE Platform

```text
01 Strength Engine
        │
        ▼
02 Temperature Engine
        │
        ▼
03 Pattern Engine
        │
        ▼
04 Useful God Engine
        │
        ▼
05 Ten Gods Engine
        │
        ▼
06 Combination Engine
        │
        ▼
07 ShenSha Engine
        │
        ▼
08 Luck Engine
        │
        ▼
09 Summary Engine
        │
        ▼
AnalysisResult
        │
        ▼
Interpretation Engine
        │
        ▼
10 Report Generator
        │
        ▼
Delivery Layer
```

The Report Generator never invokes upstream analytical stages and never modifies upstream results.

---

# 4. Architectural Principles

## 4.1 Single Responsibility

The module assembles and serializes report outputs only.

## 4.2 No Interpretation

No sentence selection, rule matching, or narrative generation occurs inside Report Generator.

## 4.3 Non-Recomputation

No analytical stage logic is re-executed inside Report Generator.

## 4.4 Non-Mutation

AnalysisResult and InterpretationResult remain immutable and unchanged.

## 4.5 Determinism

Identical assembly inputs and format profile ⇒ equivalent ReportGeneratorResult semantics.

## 4.6 Format Neutrality

StructuredReport is the canonical assembly model; format serializers derive from it.

---

# 5. Component Architecture

```text
ReportGenerator
        │
        ├── Context Validator
        ├── Upstream Result Reader
        ├── Prerequisite Validator
        ├── Structured Report Builder
        ├── Section Binder
        ├── Data Binding Adapter
        ├── Format Profile Resolver
        ├── HTML Serializer
        ├── PDF Serializer
        ├── JSON Serializer
        ├── Markdown Serializer
        ├── Report Result Builder
        └── Diagnostics Recorder
```

---

# 6. Dependency Rules

Allowed:

```text
Report Generator → ReportAssemblyContext (shared models)
Report Generator → published AnalysisResult (read-only)
Report Generator → published InterpretationResult (read-only)
Report Generator → Analysis Runtime contracts
Report Generator → presentation layout templates (layout only)
```

Forbidden:

```text
Report Generator → Interpretation Engine internals
Report Generator → upstream Analysis stage internals
Report Generator → Knowledge SDK for interpretation or domain rules
Report Generator → mutation of AnalysisResult / InterpretationResult
Report Generator → sentence library / priority engine execution
```

---

# 7. Data Flow

```text
InterpretationResult (+ optional AnalysisResult)
        │
        ▼
Report Generator assembles StructuredReport
        │
        ▼
Format serializers produce HTML / PDF / JSON / Markdown
        │
        ▼
Immutable ReportGeneratorResult
        │
        ▼
Delivery Layer
```

---

# 8. Extension Strategy

Within V1.x, additive format profiles, layout slots, and diagnostic fields are allowed without changing public API.

Public API remains:

```text
assemble(context: ReportAssemblyContext) -> ReportGeneratorResult
```

---

# 9. Constraints

- One public entry point
- No interpretation execution
- No domain knowledge execution
- No upstream semantic override
- Final assembly stage before Delivery Layer publication
