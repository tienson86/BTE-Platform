# 07_REASONING_COMPONENT.md

Version: 1.0

Status: DRAFT — Sprint B Grammar

Pack: 05 (Narrative Engine)

Component: Reasoning

Depends on: Sprint A (frozen)

---

# 1. Purpose

Reasoning states **why the observation holds** according to validated Interpretation.

It connects Observation to analytical rationale without adding new conclusions.

It answers: “Why is this the case?”

---

# 2. Responsibilities

Reasoning **must**

✓ Explain Observation using existing Interpretation / Evidence only  
✓ Keep causal links traceable to evidence refs  
✓ Stop at explanation — no action, no impact narration  

Reasoning **must not**

✗ Invent causal mechanisms absent from Interpretation/Evidence  
✗ Re-run rules or scoring  
✗ Replace Observation  
✗ Issue recommendations or warnings  

---

# 3. Inputs

| Input | Required | Role |
|-------|----------|------|
| Observation component output | **Yes** | What is being explained |
| Validated Interpretation (explanatory units) | **Yes** | Approved rationale |
| EvidenceSet | **Yes** | Trace + sufficiency |

---

# 4. Required Evidence

| Requirement | Rule |
|-------------|------|
| Link to Observation evidence | Reasoning must reference overlapping or parent evidence of Observation |
| Explanatory support | At least one Interpretation/Evidence unit classified as explanation / rationale |
| If Observation is Insufficient Evidence | Reasoning must also be Insufficient Evidence (cannot explain an empty observation) |

---

# 5. Required Interpretation

| Requirement | Rule |
|-------------|------|
| Explanatory Interpretation units | Required for non-insufficient Reasoning |
| Commercial suitability | Rule-procedure text is not Reasoning content |
| Consistency | Reasoning must not contradict Observation |

---

# 6. Output Contract

Logical section intent: `reasoning`

| Field | Rule |
|-------|------|
| `intent` | `reasoning` |
| `paragraphs[].role` | Primarily `explanation` |
| `depends_on` | Observation section id (logical dependency) |
| `evidence_refs` | Required when not insufficient |
| `insufficient_data` | True when no explanatory support |
| `recommendations` | **Empty** |

---

# 7. Narrative Position

```
Executive Summary
Observation
[Reasoning]   ← position 2
Impact
Recommendation
Warning
Conclusion
```

---

# 8. Priority

| Priority | Value |
|----------|-------|
| Flow priority | **P1 — Required** after Observation |
| Conditional | If Observation is insufficient → Reasoning insufficient (still present as shell) |

---

# 9. Failure Handling

| Condition | Handling |
|-----------|----------|
| Observation insufficient | Reasoning = Insufficient Evidence |
| Observation present, no explanatory Interpretation | Reasoning = Insufficient Evidence |
| Explanatory text technical-only | Insufficient Evidence (do not leak rule prose) |

---

# 10. Dependencies

| Depends on | Consumed by |
|------------|-------------|
| Observation | Impact, Executive Summary (optional depth), Report explanatory blocks |
| Interpretation + Evidence | — |

Must not depend on Recommendation / Warning / Conclusion.

---

# 11. Extension Points

- Multi-layer reasoning depth controlled by verbosity options  
- Theme-scoped reasoning (only with matching evidence)  

No extension may add inference beyond Interpretation.

---

# 12. Quality Rules

| Question | Answer |
|----------|--------|
| What information is required? | Explanatory Interpretation/Evidence linked to Observation |
| Why does this component exist? | Provide “why” without jumping to action |
| When should it appear? | Immediately after Observation |
| When should it be omitted? | Never silently; Insufficient Evidence if blocked |
| What should consume its output? | Impact, Portal “explanation” step, Report rationale blocks |

---

# 13. Anti-patterns

✗ Using Reasoning to introduce new chart conclusions  
✗ Scoring language (“grade becomes…”) as if Narrative recalculated  
✗ Skipping Observation and reasoning from raw Evidence only in a way that invents a new observation  
✗ Mixing impact or advice into Reasoning  

---

END
