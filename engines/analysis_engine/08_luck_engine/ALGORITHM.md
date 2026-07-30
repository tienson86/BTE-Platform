# Luck Engine Algorithm

**Module:** `engines/analysis_engine/08_luck_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Algorithm Specification)

---

# 1. Purpose

This document defines the logical algorithm of Luck evaluation.

It does not provide implementation source code.

---

# 2. Algorithm Principles

- Deterministic
- Knowledge-driven
- Evidence-based
- Hierarchy-aware (Da Yun → Liu Shi)
- Priority-aware
- No upstream recomputation
- Fail-closed on missing mandatory evidence

---

# 3. Logical Algorithm

```text
1. Validate AnalysisContext and required upstream results
2. Bind Luck Knowledge views via Knowledge SDK (frozen session)
3. Evaluate Da Yun sequence and decade-layer outcomes
4. Evaluate Liu Nian outcomes within Da Yun context
5. Evaluate Liu Yue outcomes within Liu Nian context
6. Evaluate Liu Ri outcomes within Liu Yue context
7. Evaluate Liu Shi outcomes within Liu Ri context
8. Apply luck–natal interaction profiles using published upstream evidence
9. Apply timing principles and activation rules
10. Determine favorability classes
11. Resolve priority / conflicts among competing outcomes
12. Aggregate confidence contributions
13. Build LuckResult with evidence and diagnostics
14. Return immutable result
```

---

# 4. Layer Determination

Each luck layer uses:

- chart anchor and timeline facts from AnalysisContext
- Luck Knowledge reference tables, mappings, and rules via SDK
- published natal analytical evidence where knowledge declares interaction

The engine does not invent alternate luck-layer taxonomies.

---

# 5. Interaction Determination

Interaction steps consume published Strength / Temperature / Pattern / Useful God / Ten Gods / Combination / ShenSha results as evidence classes only.

Exact interaction profiles come from Knowledge Assets, not hard-coded business rules in the algorithm contract.

---

# 6. Timing and Activation

Timing principles define when layers activate, peak, transition, or overlap.

Activation rules declare conditions under which layer effects become active.

Both are knowledge-driven.

---

# 7. Priority Resolution

When multiple outcomes compete:

1. apply declared priority classes from knowledge
2. apply conflict-resolution policy
3. record rejected alternatives as evidence/diagnostics

Resolution must be total and deterministic.

---

# 8. Confidence Aggregation

Confidence aggregates declarative contribution metadata from matched knowledge assets and layer consistency indicators.

Confidence does not replace missing mandatory upstream evidence.

---

# 9. Complexity Constraints

Algorithm steps are linear over matched luck-layer candidates for a single chart.

Unbounded non-deterministic search is forbidden.

---

# 10. Acceptance Criteria

Algorithm is accepted when logical steps, layer hierarchy, interaction boundaries, priority, and confidence rules are complete and implementation-free.
