# 05_EXECUTIVE_SUMMARY_SPEC.md

Version: 1.0

Status: DRAFT — Sprint B Grammar

Pack: 05 (Narrative Engine)

Component: Executive Summary

Depends on: Sprint A (frozen)

---

# 1. Purpose

Executive Summary is the **opening commercial overview** of the narrative.

It answers the five customer questions at summary depth:

1. Who is this person?  
2. Main strengths  
3. Main weaknesses  
4. Priority recommendation  
5. Next action  

It exists so Portal and Report can surface a complete briefing without reading every component.

---

# 2. Responsibilities

Executive Summary **must**

✓ Aggregate validated Interpretation into five summary slots  
✓ Preserve analytical meaning without alteration  
✓ Mark any slot that lacks sufficient evidence as `Insufficient Evidence`  
✓ Reference supporting component outputs or evidence ids  
✓ Appear once per NarrativeResult  

Executive Summary **must not**

✗ Infer new analytical conclusions  
✗ Score, re-grade, or re-match rules  
✗ Duplicate full Observation / Reasoning bodies  
✗ Generate sentence templates or prose assets (Sprint B forbids that)  
✗ Invent strengths, weaknesses, or actions  

---

# 3. Inputs

| Input | Required | Role |
|-------|----------|------|
| Validated InterpretationResult | **Yes** | Primary commercial source to reorganize |
| AnalysisResult evidence (via EvidenceSet) | **Yes** | Fact authority / traceability |
| Downstream component drafts (Observation…Conclusion) | Preferred | Summary may be finalized after component set is built |
| NarrativeOptions (locale, verbosity) | Optional | Depth / locale only |

---

# 4. Required Evidence

Minimum evidence kinds for a **complete** Executive Summary:

| Slot | Required evidence kinds |
|------|-------------------------|
| Identity | Day-master / pattern / strength identity signals |
| Strengths | At least one strength-class evidence unit |
| Weaknesses | At least one weakness / risk-class evidence unit |
| Priority recommendation | Useful-god / score recommendation / action-class evidence |
| Next action | Action-class evidence compatible with priority |

If any slot lacks required evidence → that slot enters **Insufficient Evidence** state.

Absence of one slot does not invent content for that slot.

---

# 5. Required Interpretation

| Requirement | Rule |
|-------------|------|
| Interpretation must be validated | Invalid Interpretation → Executive Summary cannot claim completeness |
| Interpretation sections usable | Only commercially suitable Interpretation units may fill slots |
| No raw rule-activation text | Technical Interpretation prose is not Executive content |
| Meaning lock | Executive Summary may reorder / compress Interpretation meaning; never invert it |

---

# 6. Output Contract

Logical output: `NarrativeSummary` (Sprint A model) with grammar fields:

| Field | Cardinality | State |
|-------|-------------|-------|
| `identity` | 1 | content **or** Insufficient Evidence |
| `strengths` | 1..n slots (list structure) | content **or** Insufficient Evidence |
| `weaknesses` | 1..n slots | content **or** Insufficient Evidence |
| `priority_recommendation` | 1 | content **or** Insufficient Evidence |
| `next_action` | 1 | content **or** Insufficient Evidence |
| `insufficient_flags` | 0..5 | Which slots are insufficient |
| `evidence_refs` | 0..n | Trace ids for filled slots |
| `status` | 1 | `complete` / `partial_insufficient` |

**Grammar note:** Output defines **slots and states**, not sentence wording.

---

# 7. Narrative Position

```
[Executive Summary]   ← position 0 (first)
Observation
Reasoning
Impact
Recommendation
Warning
Conclusion
```

Always the first narrative component in the official flow.

---

# 8. Priority

| Priority | Value |
|----------|-------|
| Flow priority | **P0 — Mandatory lead** |
| Omission | Never omit the component shell |
| Slot omission | Individual slots may be Insufficient Evidence; component remains present |

---

# 9. Failure Handling

| Condition | Handling |
|-----------|----------|
| No validated Interpretation | Pipeline error upstream — do not emit fake summary |
| Valid Interpretation, missing slot evidence | Slot = Insufficient Evidence; component status = `partial_insufficient` |
| Contradictory Interpretation vs AnalysisResult | Prefer AnalysisResult facts; mark conflict in metadata; do not invent reconciliation prose in Sprint B |
| All five slots insufficient | Component still emitted with all Insufficient Evidence flags |

---

# 10. Dependencies

| Depends on | Why |
|------------|-----|
| Interpretation (validated) | Source meaning to reorganize |
| EvidenceSet | Traceability and sufficiency checks |
| Observation / Strengths-Weaknesses signals | Preferred inputs for strength/weakness slots |
| Recommendation / Warning | Preferred inputs for priority and next action |

May be **drafted early** and **finalized after** Recommendation / Warning / Conclusion per Flow Spec.

---

# 11. Extension Points

- Additional optional summary metrics (never replace the five core slots)  
- Locale-specific slot ordering inside the summary (core five remain required)  
- Consultant vs customer verbosity profiles  

Extensions must not add inference.

---

# 12. Quality Rules

| Question | Answer |
|----------|--------|
| What information is required? | Five commercial slots + evidence refs / insufficient flags |
| Why does this component exist? | Give an immediate coherent briefing |
| When should it appear? | Always, first in flow |
| When should it be omitted? | Never omit component; only mark slots insufficient |
| What should consume its output? | Portal Executive Summary, Report front matter, NarrativeResult.summary |

---

# 13. Anti-patterns

✗ Writing example customer sentences in this spec  
✗ Copy-pasting full Interpretation sections into all five slots  
✗ Creating a sixth “hidden” analytical conclusion  
✗ Using Executive Summary to re-score the chart  
✗ Empty summary with no Insufficient Evidence markers  

---

END
