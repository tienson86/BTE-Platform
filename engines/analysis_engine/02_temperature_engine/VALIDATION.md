# Temperature Engine Validation

**Module:** `engines/analysis_engine/02_temperature_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Validation Specification)

---

# 1. Purpose

This document defines all validation rules performed by the Temperature Engine before, during, and after execution.

Validation ensures correctness, consistency, and integrity of analytical results.

---

# 2. Validation Strategy

Validation is performed at three stages:

1. Input Validation
2. Runtime Validation
3. Output Validation

Execution shall stop immediately when a critical validation fails.

---

# 3. Input Validation

The engine shall verify:

- AnalysisContext exists.
- StrengthResult exists.
- Required context fields are present.
- Calendar data is complete.
- Bazi pillars are complete.
- Hidden stems are available.
- StrengthResult required fields are present.
- Rule database version is supported.
- Configuration is valid.

Invalid inputs shall be rejected.

---

# 4. Runtime Validation

During execution the engine shall verify:

- Rules are successfully loaded.
- Rule categories are complete.
- Analyzer dependencies are satisfied.
- Required intermediate models are available.
- No duplicate mandatory rule execution occurs.
- StrengthResult is treated as read-only evidence.

---

# 5. Output Validation

Before publishing TemperatureResult the engine shall verify:

- Overall climate score exists.
- Temperature level exists.
- Adjustment indicators exist where required by rules.
- Confidence exists.
- Matched rules are recorded.
- Reasoning is complete.
- Metadata is attached.
- Result is immutable.

---

# 6. Model Validation

Every domain model shall define:

- required fields;
- optional fields;
- value constraints;
- invariant rules.

---

# 7. Rule Validation

Each loaded rule shall provide:

- Rule ID
- Version
- Status
- Category
- Priority

Unsupported or malformed rules shall be rejected.

---

# 8. Consistency Validation

The engine shall verify:

- deterministic execution;
- reproducible results;
- complete rule traceability;
- consistent scoring;
- no Day Master strength recomputation.

---

# 9. Failure Policy

Validation failures are classified as:

- Fatal
- Recoverable
- Warning

Only warnings allow execution to continue.

---

# 10. Acceptance Criteria

Validation is complete when:

- all required checks pass;
- no fatal validation errors remain;
- TemperatureResult satisfies all invariants.
