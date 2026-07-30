# Luck Engine Public API

**Module:** `engines/analysis_engine/08_luck_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Public API Contract)

---

# 1. Purpose

This document defines the official public interface of the Luck Engine.

---

# 2. Public Entry Point

```text
LuckEngine.evaluate(
    context: AnalysisContext
) -> LuckResult
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
- Contains published `combination_result`
- Contains published `shensha_result`
- Provides frozen KnowledgeSession / Knowledge SDK access as supplied by Analysis Runtime

Upstream results are accessed through:

```text
AnalysisContext.strength_result
AnalysisContext.temperature_result
AnalysisContext.pattern_result
AnalysisContext.useful_god_result
AnalysisContext.ten_gods_result
AnalysisContext.combination_result
AnalysisContext.shensha_result
```

---

# 4. Output Contract

```text
LuckResult
```

Shall be immutable, deterministic, explainable, and safe for downstream consumption.

---

# 5. Knowledge Access Boundary

Public API does not expose Knowledge SDK operations.

---

# 6. Error Contract

Failures surface as classified errors. No false-complete LuckResult on mandatory failure.

---

# 7. Compatibility

| Consumer | May consume LuckResult |
|----------|------------------------|
| Summary Engine | Yes |
| Interpretation Engine | Via AnalysisResult |
| Report Engine | Via AnalysisResult / Interpretation outputs |

---

# 8. Non-Public Surfaces

Internal analyzers and intermediate models are not public API.

---

# 9. Acceptance Criteria

Public API is accepted when single entry point, input/output contracts, and boundaries are complete.
