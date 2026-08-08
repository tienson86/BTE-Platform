# 08_IMPACT_COMPONENT.md

Version: 1.0

Status: DRAFT — Sprint B Grammar

Pack: 05 (Narrative Engine)

Component: Impact

Depends on: Sprint A (frozen)

---

# 1. Purpose

Impact states **what the observation/reasoning means for the person** in commercial terms already supported by Interpretation.

It answers: “So what does this mean?”

It does not prescribe the next action (Recommendation) and does not specialize risk alerts (Warning).

---

# 2. Responsibilities

Impact **must**

✓ Translate Observation + Reasoning into consequence structure  
✓ Remain within validated Interpretation impact/meaning units  
✓ Provide bridge from understanding → action components  

Impact **must not**

✗ Invent life outcomes not present in Interpretation/Evidence  
✗ Issue prioritized action lists (Recommendation)  
✗ Specialize caution blocks (Warning)  
✗ Change analytical meaning  

---

# 3. Inputs

| Input | Required | Role |
|-------|----------|------|
| Observation | **Yes** | Base facts |
| Reasoning | Preferred | Rationale bridge |
| Validated Interpretation (impact / implication units) | **Yes** for non-insufficient | Meaning units |
| EvidenceSet | **Yes** | Trace + sufficiency |

---

# 4. Required Evidence

| Requirement | Rule |
|-------------|------|
| Supported implication | At least one impact/implication-class evidence or Interpretation unit |
| Trace to Observation | Impact evidence must not float free of observed facts |
| If Observation insufficient | Impact = Insufficient Evidence |

---

# 5. Required Interpretation

| Requirement | Rule |
|-------------|------|
| Implication units | Required for filled Impact |
| No escalation beyond source | Impact severity cannot exceed Interpretation claims |
| Commercial suitability | Technical procedure text excluded |

---

# 6. Output Contract

Logical section intent: `impact`

| Field | Rule |
|-------|------|
| `intent` | `impact` |
| `paragraphs[].role` | Primarily `impact` |
| `depends_on` | Observation (required), Reasoning (preferred) |
| `evidence_refs` | Required when not insufficient |
| `insufficient_data` | True when no implication support |
| `recommendations` | **Empty** |

---

# 7. Narrative Position

```
Executive Summary
Observation
Reasoning
[Impact]   ← position 3
Recommendation
Warning
Conclusion
```

---

# 8. Priority

| Priority | Value |
|----------|-------|
| Flow priority | **P1 — Required** in official flow |
| Soft dependency | May be Insufficient Evidence if implication units missing while Observation exists |

---

# 9. Failure Handling

| Condition | Handling |
|-----------|----------|
| Observation insufficient | Impact insufficient |
| Observation present, no implication Interpretation | Impact insufficient |
| Implication contradicts Observation | Do not emit contradictory Impact; insufficient or filtered unit only |

---

# 10. Dependencies

| Depends on | Consumed by |
|------------|-------------|
| Observation, Reasoning | Recommendation, Warning, Conclusion, Executive Summary |
| Interpretation + Evidence | — |

---

# 11. Extension Points

- Domain impact facets (career / health / relationship) only as optional sub-intents with evidence  
- Severity tags as structural metadata (not new scoring)  

---

# 12. Quality Rules

| Question | Answer |
|----------|--------|
| What information is required? | Supported implication units tied to Observation |
| Why does this component exist? | Convert understanding into “what it means” |
| When should it appear? | After Reasoning, before Recommendation |
| When should it be omitted? | Never silently; use Insufficient Evidence |
| What should consume its output? | Recommendation, Warning, Conclusion, Portal “impact” step |

---

# 13. Anti-patterns

✗ Fear-mongering beyond Interpretation  
✗ Action verbs that belong in Recommendation  
✗ Treating Impact as a second Observation list  
✗ Duplicating Reasoning text unchanged under Impact label  

---

END
