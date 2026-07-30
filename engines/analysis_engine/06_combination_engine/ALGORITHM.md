# Combination Engine Algorithm

**Module:** `engines/analysis_engine/06_combination_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Algorithm Specification)

---

# 1. Purpose

This document defines the logical algorithm of Combination evaluation.

It does not provide implementation source code.

---

# 2. Algorithm Principles

- Deterministic
- Knowledge-driven
- Evidence-based
- Priority-aware
- No upstream recomputation
- Fail-closed on missing mandatory evidence

---

# 3. Logical Algorithm

```text
1. Validate AnalysisContext and required upstream results
2. Bind Combination Knowledge views via Knowledge SDK (frozen session)
3. Detect Heavenly Stem Combination candidates from chart facts + mappings
4. Detect Earthly Branch Combination candidates (pairs / triads / groups)
5. Detect Clash relations
6. Detect Harm relations
7. Detect Punishment relations
8. Detect Destruction relations
9. Detect Hidden Combination relations from hidden stems
10. Evaluate Transformation success/failure and result classes
11. Apply upstream evidence constraints where knowledge declares interaction
12. Resolve priority / conflicts among competing outcomes
13. Aggregate confidence contributions
14. Build CombinationResult with evidence and diagnostics
15. Return immutable result
```

---

# 4. Detection Determination

Detection uses:

- stem/branch positional facts from AnalysisContext
- Combination Knowledge mapping/decision/rule assets via SDK
- Fundamental stem/branch identities referenced through knowledge

The engine does not invent alternate relation taxonomies.

---

# 5. Transformation Determination

Transformation evaluation applies declarative success/failure profiles from knowledge.

Result elemental classes reference Fundamental Wu Xing identities and are not redefined by the engine.

---

# 6. Upstream Evidence Usage

Published Strength / Temperature / Pattern / Useful God / Ten Gods results may constrain or qualify combination outcomes only where Combination Knowledge declares such interaction.

They are never recomputed.

---

# 7. Priority Resolution

When multiple outcomes compete:

1. apply declared priority classes from knowledge
2. apply conflict-resolution policy
3. record rejected alternatives as evidence/diagnostics

Resolution must be total and deterministic.

---

# 8. Confidence Aggregation

Confidence aggregates declarative contribution metadata from matched knowledge assets.

Confidence does not replace missing mandatory upstream evidence.

---

# 9. Complexity Constraints

Algorithm steps are linear over matched relation candidates for a single chart.

Unbounded non-deterministic search is forbidden.

---

# 10. Acceptance Criteria

Algorithm is accepted when logical steps, transformation/priority boundaries, and confidence rules are complete and implementation-free.
