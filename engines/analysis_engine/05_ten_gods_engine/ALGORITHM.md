# Ten Gods Engine Algorithm

**Module:** `engines/analysis_engine/05_ten_gods_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Algorithm Specification)

---

# 1. Purpose

This document defines the logical algorithm of Ten Gods evaluation.

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
2. Bind Ten Gods Knowledge views via Knowledge SDK (frozen session)
3. Derive Ten Gods presence/identity structure from chart facts + knowledge
4. Evaluate relationship models among present Ten Gods
5. Apply Strength interaction profiles to presence/quality/favorability candidates
6. Apply Temperature interaction profiles where declared
7. Apply Pattern interaction profiles where declared
8. Apply Useful God interaction profiles where declared
9. Determine favorability classes
10. Attach life-area analytical concept tags (personality/career/wealth/marriage/health)
11. Collect competing outcomes and apply priority / conflict resolution
12. Aggregate confidence contributions
13. Build TenGodsResult with evidence and diagnostics
14. Return immutable result
```

---

# 4. Presence Determination

Presence/identity determination uses:

- Day Master and stem/branch relational facts
- Fundamental Ten Gods relationship identities referenced through knowledge
- Ten Gods Knowledge definition/mapping assets via SDK

The engine does not invent alternate Ten Gods taxonomies.

---

# 5. Interaction Determination

Interaction steps consume published upstream classifications as evidence classes only.

Example logical effect:

- strong/weak body class may alter favorability of output/officer/resource classes per knowledge
- pattern identity may constrain structural Ten Gods readings per knowledge
- useful god roles may reinforce or oppose Ten Gods favorability per knowledge

Exact weights/profiles come from Knowledge Assets, not hard-coded business rules in the algorithm contract.

---

# 6. Priority Resolution

When multiple outcomes compete:

1. apply declared priority classes from knowledge
2. apply conflict-resolution policy
3. record rejected alternatives as evidence/diagnostics

Resolution must be total and deterministic.

---

# 7. Confidence Aggregation

Confidence aggregates declarative contribution metadata from matched knowledge assets and interaction consistency indicators.

Confidence does not replace missing mandatory upstream evidence.

---

# 8. Complexity Constraints

Algorithm steps are linear over matched knowledge candidates for a single chart.

Unbounded non-deterministic search is forbidden.

---

# 9. Acceptance Criteria

Algorithm is accepted when logical steps, interaction boundaries, priority, and confidence rules are complete and implementation-free.
