# Temperature Engine Public API

**Module:** `engines/analysis_engine/02_temperature_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Public API Contract)

---

# 1. Purpose

This document defines the official public interface of the Temperature Engine.

Only the interfaces described here are guaranteed to remain stable throughout the V1.x lifecycle.

Internal components are not part of the public contract.

---

# 2. Public Entry Point

The module exposes exactly one public operation.

```text
TemperatureEngine.evaluate(context, strength)
```

No additional execution entry points are guaranteed.

---

# 3. Input Contract

Input Types:

```text
AnalysisContext
StrengthResult
```

Requirements:

- Immutable
- Validated
- Complete
- AnalysisContext produced by upstream Calendar and Bazi stages
- StrengthResult produced by the Strength Engine

The Temperature Engine shall reject invalid inputs.

---

# 4. Output Contract

Output Type:

```text
TemperatureResult
```

The returned object shall be:

- Immutable
- Explainable
- Deterministic
- Fully validated

---

# 5. Execution Contract

The API guarantees:

- deterministic execution
- rule-based evaluation
- immutable outputs
- explainable decisions
- thread-safe execution
- no Day Master strength recomputation

---

# 6. Error Contract

The API may return errors for:

- invalid context
- invalid or missing StrengthResult
- missing rules
- unsupported versions
- invalid runtime configuration
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

---

# 11. Usage Rules

Consumers shall:

- treat returned models as immutable
- never modify AnalysisContext after submission
- never modify StrengthResult after submission
- never depend on internal implementation
- rely only on documented contracts

---

# 12. Compatibility Matrix

| Consumer | Supported |
|-----------|-----------|
| Pattern Engine | ✓ |
| Useful God Engine | ✓ |
| Ten Gods Engine | ✓ |
| Combination Engine | ✓ |
| ShenSha Engine | ✓ |
| Luck Engine | ✓ |
| Summary Engine | ✓ |
| Interpretation Engine | ✓ |

All consumers interact exclusively through the documented public API.
