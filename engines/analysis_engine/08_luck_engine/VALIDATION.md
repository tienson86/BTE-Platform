# Luck Engine Validation

**Module:** `engines/analysis_engine/08_luck_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Validation Specification)

---

# 1. Purpose

This document defines validation requirements for Luck Engine execution.

---

# 2. Validation Levels

1. Input Context Validation
2. Upstream Result Presence Validation
3. Knowledge Session Validation
4. Precondition Validation
5. Layer Hierarchy Validation
6. Intermediate Consistency Validation
7. Result Schema Validation
8. Explainability Validation
9. Final Publication Validation

---

# 3. Input Context Validation

Verify AnalysisContext is present, immutable/request-ready, and contains required chart facts including timeline anchors where declared.

---

# 4. Upstream Result Presence Validation

Require non-null published:

- strength_result
- temperature_result
- pattern_result
- useful_god_result
- ten_gods_result
- combination_result
- shensha_result

Missing any required upstream result fails closed.

---

# 5. Knowledge Session Validation

Verify Knowledge SDK session provides load-eligible Luck Knowledge for the frozen request versions.

Compatibility/integrity failures fail closed.

---

# 6. Precondition Validation

Verify stage readiness according to Analysis Runtime pipeline position (stage 08).

---

# 7. Layer Hierarchy Validation

Verify Da Yun → Liu Nian → Liu Yue → Liu Ri → Liu Shi nesting is respected in intermediate and final outputs.

---

# 8. Intermediate Consistency Validation

Verify layer outcomes reference only declared knowledge identities and published upstream evidence classes.

---

# 9. Result Schema Validation

Verify LuckResult contains required structural fields and legal enumerations for all five luck layers.

---

# 10. Explainability Validation

Verify material determinations include KnowledgeReferences / evidence as required.

---

# 11. Final Publication Validation

Verify result immutability readiness and readiness for AnalysisContext publication.

---

# 12. Failure Behavior

Mandatory validation failures raise classified errors and prevent successful LuckResult publication.

---

# 13. Acceptance Criteria

Validation is accepted when levels, required upstream checks, layer hierarchy checks, and fail-closed behavior are complete.
