# Report Generator Validation

**Module:** `engines/analysis_engine/10_report_generator`  
**Version:** V1.0.0  
**Status:** Frozen (Validation Specification)

---

# 1. Purpose

This document defines validation requirements for Report Generator execution.

---

# 2. Validation Levels

1. Input Context Validation
2. InterpretationResult Validation
3. AnalysisResult Validation (when required)
4. Format Profile Validation
5. Assembly Prerequisite Validation
6. StructuredReport Schema Validation
7. Format Artifact Validation
8. Result Schema Validation
9. Final Publication Validation

---

# 3. Input Context Validation

Verify ReportAssemblyContext is present, immutable/request-ready, and pipeline-complete for stage 10.

---

# 4. InterpretationResult Validation

Require non-null published InterpretationResult with mandatory interpreted sections declared by format profile.

Missing mandatory interpretation content fails closed.

---

# 5. AnalysisResult Validation

When format profile requires structured analytical sections:

- verify non-null published AnalysisResult
- verify required stage result slots are present
- verify schema conformance

When profile is interpretation-only, AnalysisResult absence is permitted.

---

# 6. Format Profile Validation

Verify format profile declares legal output formats and layout policy.

At least one output format must be requested.

Full publication profile requires HTML, PDF, JSON, Markdown, and StructuredReport.

---

# 7. Assembly Prerequisite Validation

Verify all required section bindings and structured data bindings can be resolved without semantic invention.

---

# 8. StructuredReport Schema Validation

Verify StructuredReport contains required structural fields, legal section ordering, and trace references.

---

# 9. Format Artifact Validation

Verify each requested format artifact:

- is present
- conforms to format schema
- derives from the same StructuredReport
- contains no uninvented interpretive content

---

# 10. Result Schema Validation

Verify ReportGeneratorResult contains required fields and legal enumerations for declared profile.

---

# 11. Final Publication Validation

Verify result immutability readiness and readiness for Delivery Layer consumption.

---

# 12. Failure Behavior

Mandatory validation failures raise classified errors and prevent successful ReportGeneratorResult publication.

---

# 13. Acceptance Criteria

Validation is accepted when levels, prerequisite checks, format rules, and fail-closed behavior are complete.
