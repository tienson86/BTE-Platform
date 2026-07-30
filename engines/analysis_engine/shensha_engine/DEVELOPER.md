# ShenSha Engine — Implementation Guide

**Module:** `engines.analysis_engine.shensha_engine`  
**Architecture docs:** `engines/analysis_engine/07_shensha_engine/`  
**Version:** 1.0.0  
**Status:** Implementation Baseline

---

# 1. Purpose

This document describes the Python implementation of Analysis Engine stage 07 (ShenSha).

It complements the frozen architecture documentation set under `07_shensha_engine/`.

---

# 2. Package Layout

```text
engines/analysis_engine/shensha_engine/
  __init__.py
  engine.py              # ShenShaEngine (Runtime module)
  models.py              # ShenShaResult and domain models
  calculator.py          # Deterministic knowledge-driven evaluation
  validators.py          # Context / upstream / knowledge / result validation
  knowledge_access.py    # Knowledge SDK session contract
  default_knowledge.py   # Deterministic default knowledge pack
  exceptions.py          # Stage error classes
```

Python cannot import `07_shensha_engine` as a package name (leading digit).  
Importable package: `engines.analysis_engine.shensha_engine`.

---

# 3. Public API

```python
from engines.analysis_engine.shensha_engine import (
    ShenShaEngine,
    ShenShaResult,
    create_default_knowledge_session,
)

engine = ShenShaEngine()
stage_result = engine.evaluate(context)       # Runtime StageResult
typed = engine.evaluate_shensha(context)      # ShenShaResult
ShenShaResult.from_stage_result(stage_result)
```

---

# 4. Inputs / Outputs

## Consumes

| Input | Source |
|-------|--------|
| AnalysisContext | Analysis Runtime |
| Strength → Combination results | `AnalysisContext.*_result` |
| ShenSha Knowledge | `AnalysisContext.knowledge_session` (SDK) |

## Produces

| Output | Form |
|--------|------|
| ShenShaResult | Domain model in `StageResult.payload` |

---

# 5. Knowledge SDK

Logical module identity:

```text
shensha_knowledge
```

Required assets (default pack):

- `shensha.calculation_references`
- `shensha.lookup_tables`
- `shensha.mapping_tables`
- `shensha.identities`
- `shensha.interactions`
- `shensha.compatibility`
- `shensha.exceptions`
- `shensha.upstream_qualifiers`
- `shensha.priority`
- `shensha.confidence`

Bind a session before evaluation:

```python
context.knowledge_session = create_default_knowledge_session()
```

Or via Analysis Runtime `knowledge_binder`.

---

# 6. Algorithm Summary

1. Validate context and upstream results  
2. Bind ShenSha knowledge via SDK  
3. Resolve calculation anchors (day stem, year/day branch)  
4. Apply lookup tables → presence candidates  
5. Map identities and polarity (auspicious / inauspicious / conditional)  
6. Evaluate interactions and compatibility  
7. Apply exception overrides / suppressions  
8. Apply upstream qualifiers where declared  
9. Aggregate confidence and publish `ShenShaResult`

---

# 7. Runtime Registration

```python
from engines.analysis_engine.runtime import AnalysisRuntime
from engines.analysis_engine.shensha_engine import (
    ShenShaEngine,
    create_default_knowledge_session,
)

runtime = AnalysisRuntime(
    require_all_canonical_stages=False,
    knowledge_binder=lambda ctx: setattr(
        ctx, "knowledge_session", create_default_knowledge_session()
    ),
)
runtime.register(ShenShaEngine())
```

Dependencies (canonical):

```text
strength → temperature → pattern → useful_god → ten_gods → combination → shensha
```

---

# 8. Testing

```bash
pytest tests/shensha_engine -q
```

---

# 9. Boundaries

| In scope | Out of scope |
|----------|--------------|
| ShenSha detection / classification | Upstream recomputation |
| Interactions / exceptions / confidence | Interpretation narrative |
| SDK-only knowledge access | Report rendering |

---

# 10. Version

Implementation version: **1.0.0**  
Aligned with ShenSha Engine Architecture Baseline V1.0.0.
