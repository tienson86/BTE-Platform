# Ten Gods Engine Public API

**Module:** `engines/analysis_engine/05_ten_gods_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Public API Contract)

---

# 1. Purpose

This document defines the official public interface of the Ten Gods Engine.

Only the interfaces described here are guaranteed to remain stable throughout the V1.x lifecycle.

---

# 2. Public Entry Point

The module exposes exactly one public operation.

```text
TenGodsEngine.evaluate(
    context: AnalysisContext
) -> TenGodsResult
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
- Produced by upstream Calendar and BaZi stages
- Contains published `strength_result`
- Contains published `temperature_result`
- Contains published `pattern_result`
- Contains published `useful_god_result`
- Provides access to frozen KnowledgeSession / Knowledge SDK handles as supplied by Analysis Runtime

Upstream results are accessed through:

```text
AnalysisContext.strength_result
AnalysisContext.temperature_result
AnalysisContext.pattern_result
AnalysisContext.useful_god_result
```

The Ten Gods Engine shall reject invalid inputs.

---

# 4. Output Contract

Output Type:

```text
TenGodsResult
```

The returned object shall be:

- Immutable
- Deterministic for identical inputs and frozen knowledge versions
- Explainable
- Serializable under shared Analysis Engine conventions
- Safe for downstream consumption without re-derivation

---

# 5. Knowledge Access Boundary

Public API does not expose Knowledge SDK operations.

Knowledge access is an internal concern of the engine under Analysis Runtime session binding.

---

# 6. Error Contract

Failures surface as classified stage/runtime errors aligned with Analysis Runtime Error Model and Ten Gods Error Handling specification.

No false-complete TenGodsResult on mandatory failure.

---

# 7. Compatibility

| Consumer | May consume TenGodsResult |
|----------|---------------------------|
| Combination Engine | Yes |
| ShenSha Engine | Yes (where declared) |
| Luck Engine | Yes (where declared) |
| Summary Engine | Yes |
| Interpretation Engine | Via AnalysisResult |
| Report Engine | Via AnalysisResult / Interpretation outputs |

---

# 8. Non-Public Surfaces

Internal analyzers, intermediate models, and SDK accessors are not public API.

---

# 9. Acceptance Criteria

Public API is accepted when single entry point, input/output contracts, and boundaries are complete.
