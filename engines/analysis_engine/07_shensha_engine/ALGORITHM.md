# ShenSha Engine Algorithm

**Module:** `engines/analysis_engine/07_shensha_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Algorithm Specification)

---

# 1. Purpose

This document defines the logical algorithm of ShenSha evaluation.

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
2. Bind ShenSha Knowledge views via Knowledge SDK (frozen session)
3. Resolve calculation references from chart anchors
4. Apply lookup tables to derive ShenSha presence keys
5. Apply mapping tables to assign ShenSha identities and polarity
6. Classify Auspicious and Inauspicious ShenSha
7. Evaluate interaction rules among co-present identities
8. Evaluate compatibility classes
9. Apply exception overrides / suppressions
10. Apply upstream evidence constraints where knowledge declares interaction
11. Resolve priority / conflicts among competing outcomes
12. Aggregate confidence contributions
13. Build ShenShaResult with evidence and diagnostics
14. Return immutable result
```

---

# 4. Detection Determination

Detection uses:

- chart anchor facts (Year / Month / Day / Hour as declared by knowledge)
- stem / branch / hidden-stem facts from AnalysisContext
- ShenSha Knowledge calculation references, lookup tables, and mapping tables via SDK

The engine does not invent alternate ShenSha taxonomies.

---

# 5. Interaction and Exception Determination

Interaction and exception steps apply declarative knowledge profiles.

Co-present ShenSha identities may produce interaction outcomes per knowledge.

Exception conditions may override or suppress default outcomes per knowledge.

---

# 6. Upstream Evidence Usage

Published Strength / Temperature / Pattern / Useful God / Ten Gods / Combination results may constrain or qualify ShenSha outcomes only where ShenSha Knowledge declares such interaction.

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

Algorithm steps are linear over matched ShenSha candidates for a single chart.

Unbounded non-deterministic search is forbidden.

---

# 10. Acceptance Criteria

Algorithm is accepted when logical steps, interaction/exception boundaries, priority, and confidence rules are complete and implementation-free.
