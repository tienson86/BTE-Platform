# Summary Engine Public API

**Module:** `engines/analysis_engine/09_summary_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Public API Contract)

---

# 1. Purpose

This document defines the official public interface of the Summary Engine.

---

# 2. Public Entry Point

```text
SummaryEngine.evaluate(
    context: AnalysisContext
) -> SummaryResult
```

No additional public methods are exposed.

No multi-parameter APIs are permitted.

Upstream stage results must not be passed as separate parameters.

---

# 3. Input Contract

Input Type:

```text
AnalysisContext
```

Requirements:

- Immutable
- Validated
- Complete
- Contains published results for all mandatory upstream stages

Upstream results are accessed through:

```text
AnalysisContext.strength_result
AnalysisContext.temperature_result
AnalysisContext.pattern_result
AnalysisContext.useful_god_result
AnalysisContext.ten_gods_result
AnalysisContext.combination_result
AnalysisContext.shensha_result
AnalysisContext.luck_result
```

---

# 4. Output Contract

```text
SummaryResult
```

Shall be immutable, deterministic, explainability-preserving, and safe for downstream consumption.

---

# 5. Aggregation Boundary

Public API does not expose individual upstream stage results separately.

Consolidation reads from AnalysisContext only.

---

# 6. Error Contract

Failures surface as classified errors. No false-complete SummaryResult on mandatory failure.

---

# 7. Compatibility

| Consumer | May consume SummaryResult |
|----------|---------------------------|
| Analysis Runtime (AnalysisResult assembly) | Yes |
| Interpretation Engine | Via AnalysisResult |
| Report Engine | Via AnalysisResult / Interpretation outputs |

---

# 8. Non-Public Surfaces

Internal aggregators and intermediate models are not public API.

---

# 9. Acceptance Criteria

Public API is accepted when single entry point, input/output contracts, and boundaries are complete.
