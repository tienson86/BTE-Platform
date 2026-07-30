# Report Generator Error Handling

**Module:** `engines/analysis_engine/10_report_generator`  
**Version:** V1.0.0  
**Status:** Frozen (Error Handling Specification)

---

# 1. Purpose

This document defines error classification and handling for the Report Generator.

---

# 2. Error Principles

- Fail closed
- Explicit classification
- No silent omission of mandatory formats
- No interpretation as recovery
- No upstream recomputation as recovery
- No mutation of upstream results as recovery
- Align with Analysis Runtime Error Model

---

# 3. Error Classes

| Class | Typical Cause |
|-------|---------------|
| ValidationError | Invalid ReportAssemblyContext |
| PrerequisiteError | Missing InterpretationResult or required AnalysisResult |
| FormatProfileError | Invalid or unsupported format profile |
| BindingError | Unresolvable section or structured data binding |
| SerializationError | Format serializer failure |
| SchemaError | StructuredReport or artifact schema mismatch |
| ExecutionError | Internal assembly failure |
| StateError | Illegal invocation/lifecycle usage |

---

# 4. Error Surface

Errors shall include:

- error class
- stage identity (`report_generator`)
- missing upstream field identity when applicable
- format identity when applicable
- binding/serialization summary when applicable
- summary
- retryability flag

---

# 5. Recovery Policy

## Allowed

- whole-stage retry under Analysis Runtime governed retry policy when upstream results may become available on retry

## Forbidden

- generate interpretive text without InterpretationResult
- patch InterpretationResult or AnalysisResult to force assembly
- publish ReportGeneratorResult with missing mandatory format artifacts
- invoke Interpretation Engine locally as fallback
- recompute analytical stages locally

---

# 6. Propagation

Errors propagate to Analysis Runtime orchestrator.

No successful ReportGeneratorResult is returned on mandatory failure.

Delivery Layer does not receive report artifacts when Report Generator fails.

---

# 7. Acceptance Criteria

Error Handling is accepted when classes, surface, recovery allow/forbid rules, and propagation are complete.
