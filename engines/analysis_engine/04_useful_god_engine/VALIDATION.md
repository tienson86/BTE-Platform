# Useful God Engine Validation

**Module:** `engines/analysis_engine/04_useful_god_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Validation Specification)

---

# 1. Purpose

This document defines all validation rules performed by the Useful God Engine before, during, and after execution.

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
- AnalysisContext.strength_result exists.
- AnalysisContext.temperature_result exists.
- AnalysisContext.pattern_result exists.
- Required context fields are present.
- Calendar data is complete.
- Bazi pillars are complete.
- Hidden stems are available.
- StrengthResult required fields are present within AnalysisContext.
- TemperatureResult required fields are present within AnalysisContext.
- PatternResult required fields are present within AnalysisContext.
- Rule database version is supported.
- Configuration is valid.

Invalid inputs shall be rejected.

---

# 4. Runtime Validation

During execution the engine shall verify:

- Rules are successfully loaded from the Useful God Rule Database Knowledge Module.
- Rule categories are complete for mandatory Useful God categories.
- Analyzer dependencies are satisfied.
- Required intermediate models are available.
- Candidate generation produces a valid candidate set.
- No duplicate mandatory rule execution occurs.
- AnalysisContext.strength_result is treated as read-only evidence.
- AnalysisContext.temperature_result is treated as read-only evidence.
- AnalysisContext.pattern_result is treated as read-only evidence.

---

# 5. Output Validation

Before publishing UsefulGodResult the engine shall verify:

- useful_god exists.
- favorable_gods exists.
- unfavorable_gods exists.
- neutral_gods exists.
- Candidate rankings exist.
- Confidence exists.
- Matched rules are recorded.
- Rejected candidates are recorded.
- Reasoning is complete.
- Diagnostics are attached.
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
- no Strength recomputation;
- no Temperature recomputation;
- no Pattern recomputation.

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
- UsefulGodResult satisfies all invariants.
