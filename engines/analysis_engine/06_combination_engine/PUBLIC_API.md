# Combination Engine Public API

**Module:** `engines/analysis_engine/06_combination_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Public API Contract)

---

# 1. Purpose

This document defines the official public interface of the Combination Engine.

---

# 2. Public Entry Point

```text
CombinationEngine.evaluate(
    context: AnalysisContext
) -> CombinationResult
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
- Contains published `strength_result`
- Contains published `temperature_result`
- Contains published `pattern_result`
- Contains published `useful_god_result`
- Contains published `ten_gods_result`
- Provides frozen KnowledgeSession / Knowledge SDK access as supplied by Analysis Runtime

Upstream results are accessed through:

```text
AnalysisContext.strength_result
AnalysisContext.temperature_result
AnalysisContext.pattern_result
AnalysisContext.useful_god_result
AnalysisContext.ten_gods_result
```

---

# 4. Output Contract

```text
CombinationResult
```

Shall be immutable, deterministic, explainable, and safe for downstream consumption.

---

# 5. Knowledge Access Boundary

Public API does not expose Knowledge SDK operations.

---

# 6. Error Contract

Failures surface as classified errors. No false-complete CombinationResult on mandatory failure.

---

# 7. Compatibility

| Consumer | May consume CombinationResult |
|----------|-------------------------------|
| ShenSha Engine | Yes (where declared) |
| Luck Engine | Yes (where declared) |
| Summary Engine | Yes |
| Interpretation Engine | Via AnalysisResult |
| Report Engine | Via AnalysisResult / Interpretation outputs |

---

# 8. Non-Public Surfaces

Internal analyzers and intermediate models are not public API.

---

# 9. Acceptance Criteria

Public API is accepted when single entry point, input/output contracts, and boundaries are complete.
