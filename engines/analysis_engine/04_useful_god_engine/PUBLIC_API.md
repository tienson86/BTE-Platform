# Useful God Engine Public API

**Module:** `engines/analysis_engine/04_useful_god_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Public API Contract)

---

# 1. Purpose

This document defines the official public interface of the Useful God Engine.

Only the interfaces described here are guaranteed to remain stable throughout the V1.x lifecycle.

Internal components are not part of the public contract.

---

# 2. Public Entry Point

The module exposes exactly one public operation.

```text
UsefulGodEngine.evaluate(
    context: AnalysisContext
) -> UsefulGodResult
```

No additional public methods are exposed.

No multi-parameter APIs are permitted.

No additional execution entry points are guaranteed.

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
- Contains published `strength_result` from the Strength Engine
- Contains published `temperature_result` from the Temperature Engine
- Contains published `pattern_result` from the Pattern Engine

Upstream results are accessed through:

```text
AnalysisContext.strength_result
AnalysisContext.temperature_result
AnalysisContext.pattern_result
```

The Useful God Engine shall not accept upstream stage results as separate function parameters.

No dedicated input wrapper models shall be introduced.

The Useful God Engine shall reject invalid inputs.

---

# 4. Output Contract

Output Type:

```text
UsefulGodResult
```

The returned object shall be:

- Immutable
- Explainable
- Deterministic
- Fully validated

UsefulGodResult becomes part of AnalysisResult.

Minimum content:

- useful_god
- favorable_gods
- unfavorable_gods
- neutral_gods
- candidate rankings
- confidence
- matched rules
- rejected candidates
- reasoning
- diagnostics
- metadata

---

# 5. Execution Contract

The API guarantees:

- deterministic execution
- rule-based evaluation
- immutable outputs
- explainable decisions
- thread-safe execution
- no Strength recomputation
- no Temperature recomputation
- no Pattern recomputation

---

# 6. Error Contract

The API may return errors for:

- invalid context
- missing or invalid AnalysisContext.strength_result
- missing or invalid AnalysisContext.temperature_result
- missing or invalid AnalysisContext.pattern_result
- missing rules
- unsupported versions
- invalid runtime configuration
- unresolvable Useful God candidate conflicts
- analytical failures

Errors shall not modify input data.

---

# 7. Version Contract

The API is stable within V1.x.

Breaking interface changes require a new major version.

---

# 8. Thread Safety

The public API is designed for concurrent execution.

The implementation shall remain stateless.

---

# 9. Performance Contract

Expected characteristics:

- deterministic runtime
- cache-friendly
- low allocation
- scalable execution

Performance optimizations must not change analytical behavior.

---

# 10. Extension Policy

Future versions may add optional capabilities.

Existing API behavior shall remain unchanged within V1.x.

Additional public methods are prohibited within V1.x.

---

# 11. Usage Rules

Consumers shall:

- treat returned models as immutable
- never modify AnalysisContext after submission
- never depend on internal implementation
- rely only on documented contracts

---

# 12. Compatibility Matrix

| Consumer | Supported |
|-----------|-----------|
| Ten Gods Engine | ✓ |
| Combination Engine | ✓ |
| ShenSha Engine | ✓ |
| Luck Engine | ✓ |
| Summary Engine | ✓ |
| Interpretation Engine | ✓ |

All consumers interact exclusively through the documented public API.
