# Analysis Engine Public API

**Module:** `engines/analysis_engine`  
**Version:** 1.0.0  
**Status:** Frozen (Public API Contract)

---

# 1. Purpose

This document defines the public interface of the Analysis Engine.

Consumers interact only with the orchestration layer and the published AnalysisResult.

---

# 2. Public Entry Point

The module exposes one public operation:

```text
AnalysisEngine.evaluate(context: AnalysisContext) -> AnalysisResult
```

---

# 3. Input Contract

Input:

- AnalysisContext

Requirements:

- immutable;
- validated;
- produced by upstream engines.

---

# 4. Output Contract

Output:

- AnalysisResult

The result is immutable and contains all published stage outputs.

---

# 5. Execution Guarantees

The API guarantees:

- deterministic execution;
- ordered pipeline;
- immutable outputs;
- explainable results;
- thread-safe orchestration.

---

# 6. Error Contract

Possible failures include:

- invalid context;
- pipeline failure;
- rule incompatibility;
- configuration errors.

Errors are standardized across all stages.

---

# 7. Versioning

Public API stability is guaranteed within Version 1.x.

Breaking interface changes require Version 2.