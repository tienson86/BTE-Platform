# Ten Gods Engine Validation

**Module:** `engines/analysis_engine/05_ten_gods_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Validation Specification)

---

# 1. Purpose

This document defines validation requirements for Ten Gods Engine execution.

---

# 2. Validation Levels

1. Input Context Validation
2. Upstream Result Presence Validation
3. Knowledge Session Validation
4. Precondition Validation
5. Intermediate Consistency Validation
6. Result Schema Validation
7. Explainability Validation
8. Final Publication Validation

---

# 3. Input Context Validation

Verify AnalysisContext is present, immutable/request-ready, and contains required chart facts.

---

# 4. Upstream Result Presence Validation

Require non-null published:

- strength_result
- temperature_result
- pattern_result
- useful_god_result

Missing any required upstream result fails closed.

---

# 5. Knowledge Session Validation

Verify Knowledge SDK session provides load-eligible Ten Gods Knowledge for the frozen request versions.

Compatibility/integrity failures fail closed.

---

# 6. Precondition Validation

Verify stage readiness according to Analysis Runtime pipeline position (stage 05).

---

# 7. Intermediate Consistency Validation

Verify interaction analyses reference only published upstream evidence classes and declared knowledge identities.

---

# 8. Result Schema Validation

Verify TenGodsResult contains required structural fields and legal enumerations.

---

# 9. Explainability Validation

Verify material determinations include KnowledgeReferences / evidence as required by stage contracts.

---

# 10. Final Publication Validation

Verify result immutability readiness and readiness for AnalysisContext publication.

---

# 11. Failure Behavior

Mandatory validation failures raise classified errors and prevent successful TenGodsResult publication.

---

# 12. Acceptance Criteria

Validation is accepted when levels, required upstream checks, and fail-closed behavior are complete.
