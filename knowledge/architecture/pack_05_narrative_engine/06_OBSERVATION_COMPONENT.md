# 06_OBSERVATION_COMPONENT.md

Version: 1.0

Status: DRAFT — Sprint B Grammar

Pack: 05 (Narrative Engine)

Component: Observation

Depends on: Sprint A (frozen)

---

# 1. Purpose

Observation states **what is seen** in the validated Interpretation / evidence — the factual narrative stance.

It answers: “What do we observe about this chart?”

It does not explain why, does not judge impact, and does not recommend action.

---

# 2. Responsibilities

Observation **must**

✓ Present observable analytical facts in narrative structure  
✓ Stay faithful to Interpretation + Evidence  
✓ Provide the factual base for Reasoning and Impact  
✓ Emit Insufficient Evidence when observation facts are missing  

Observation **must not**

✗ Explain causality (Reasoning owns that)  
✗ State life impact (Impact owns that)  
✗ Recommend actions (Recommendation owns that)  
✗ Warn about risks as a dedicated warning block (Warning owns that)  
✗ Infer unseen facts  

---

# 3. Inputs

| Input | Required | Role |
|-------|----------|------|
| Validated Interpretation (identity / overview units) | **Yes** | Observable claims to reorganize |
| EvidenceSet (identity, pattern, strength, element signals) | **Yes** | Sufficiency + tracing |
| NarrativeOptions | Optional | Verbosity |

---

# 4. Required Evidence

At least one of:

| Evidence kind | Use |
|---------------|-----|
| Identity (day master / chart identity) | Core observation |
| Pattern / structure | Core observation |
| Strength level / score band | Supporting observation |
| Five-element / ten-god prominence | Supporting observation |

If none available → Observation = **Insufficient Evidence**.

---

# 5. Required Interpretation

| Requirement | Rule |
|-------------|------|
| Validated Interpretation present | Required for commercial Observation |
| Observable units only | Use Interpretation content that states facts, not rule procedures |
| No meaning change | Observation may compress; must not reverse facts |

---

# 6. Output Contract

Logical section intent: `observation`

| Field | Rule |
|-------|------|
| `intent` | `observation` |
| `paragraphs[].role` | Primarily `observation` |
| `evidence_refs` | Required when not insufficient |
| `insufficient_data` | True when evidence missing |
| `recommendations` | **Empty** (forbidden here) |

Grammar forbids mixing recommendation/warning roles into Observation paragraphs.

---

# 7. Narrative Position

```
Executive Summary
[Observation]   ← position 1
Reasoning
Impact
Recommendation
Warning
Conclusion
```

---

# 8. Priority

| Priority | Value |
|----------|-------|
| Flow priority | **P1 — Required** when Interpretation has observable facts |
| Omission | Omit only if entire narrative aborted; otherwise emit Insufficient Evidence shell |

---

# 9. Failure Handling

| Condition | Handling |
|-----------|----------|
| No observable evidence | `insufficient_data = true` |
| Only technical rule prose available | Treat as unsuitable → Insufficient Evidence (do not pass rule prose) |
| Conflict between sources | Prefer AnalysisResult evidence; do not invent merge |

---

# 10. Dependencies

| Upstream | Downstream consumers |
|----------|----------------------|
| Interpretation + Evidence | Reasoning, Impact, Executive Summary (identity) |

Observation has **no** dependency on Recommendation / Warning / Conclusion.

---

# 11. Extension Points

- Optional sub-observations (career/relationship) only when evidence kinds exist  
- Verbosity profiles controlling observation count — not new facts  

---

# 12. Quality Rules

| Question | Answer |
|----------|--------|
| What information is required? | Observable chart facts with evidence refs |
| Why does this component exist? | Establish “what is seen” before why/impact/action |
| When should it appear? | Always in official order after Executive Summary |
| When should it be omitted? | Never silently; use Insufficient Evidence |
| What should consume its output? | Reasoning, Impact, Portal interpretation “observation” step, Report body |

---

# 13. Anti-patterns

✗ Turning Observation into a full mini-report  
✗ Embedding “you should…” actions  
✗ Embedding causal “because…” chains (belongs in Reasoning)  
✗ Duplicating raw Evidence tables as narrative  
✗ Repeating entire Interpretation section verbatim without reorganization  

---

END
