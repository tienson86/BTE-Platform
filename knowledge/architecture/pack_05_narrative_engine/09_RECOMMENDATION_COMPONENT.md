# 09_RECOMMENDATION_COMPONENT.md

Version: 1.0

Status: DRAFT — Sprint B Grammar

Pack: 05 (Narrative Engine)

Component: Recommendation

Depends on: Sprint A (frozen)

---

# 1. Purpose

Recommendation states **what the person should prioritize doing**, based only on validated Interpretation and Evidence.

It answers: “What should be done?” and supports Executive Summary slots:

- Priority recommendation  
- Next action  

---

# 2. Responsibilities

Recommendation **must**

✓ Structure action guidance already present in Interpretation / Evidence  
✓ Assign semantic priority levels without recalculating scores  
✓ Feed Executive Summary action slots  
✓ Emit Insufficient Evidence when no action support exists  

Recommendation **must not**

✗ Invent actions unsupported by Interpretation/Evidence  
✗ Recompute useful god / grades  
✗ Replace Warning (risk caution is separate)  
✗ Narrate full Observation/Reasoning again  

---

# 3. Inputs

| Input | Required | Role |
|-------|----------|------|
| Impact (preferred) | Preferred | Context for why action matters |
| Observation | Preferred | Anchors action to facts |
| Validated Interpretation (action / useful-god / counsel units) | **Yes** for filled recommendations | Action meaning |
| EvidenceSet (action / useful-god / score.recommendation) | **Yes** | Sufficiency + tracing |

---

# 4. Required Evidence

For a **filled** Recommendation component:

| Evidence | Rule |
|----------|------|
| Action-class evidence **or** | Minimum one |
| Useful-god / favorable guidance evidence **or** | Minimum one |
| Score recommendation field mapped as evidence | Allowed as action support |

If none → Recommendation = **Insufficient Evidence**.

Priority ordering among multiple actions uses Interpretation/Evidence priority metadata only — Narrative does not invent a new ranking algorithm beyond declared source priority.

---

# 5. Required Interpretation

| Requirement | Rule |
|-------------|------|
| Actionable Interpretation units | Required for non-insufficient output |
| Alignment with Impact/Observation | Actions must not contradict observed meaning |
| Commercial suitability | Exclude technical procedure text |

---

# 6. Output Contract

Logical section intent: `recommendation`

Uses Sprint A model `NarrativeRecommendation`:

| Field | Rule |
|-------|------|
| `intent` | `recommendation` |
| `recommendations[]` | 1..n when filled; empty + insufficient flag when not |
| `priority` | critical / high / medium / low (semantic) |
| `action` / `reason` / `benefit` | Structural slots — wording not specified in Sprint B |
| `evidence_refs` | Required per recommendation when filled |
| `insufficient_data` | Component-level and/or item-level |

Paragraph roles may include `suggestion` only inside this component.

---

# 7. Narrative Position

```
Executive Summary
Observation
Reasoning
Impact
[Recommendation]   ← position 4
Warning
Conclusion
```

---

# 8. Priority

| Priority | Value |
|----------|-------|
| Flow priority | **P0 — Commercially mandatory shell** |
| Content priority | Highest semantic priority item feeds Executive Summary `priority_recommendation` |
| Next action | Distinct slot; may equal top recommendation or immediate follow-on from Interpretation |

---

# 9. Failure Handling

| Condition | Handling |
|-----------|----------|
| No action evidence | Insufficient Evidence |
| Action contradicts Impact | Drop contradictory unit; do not invent fix |
| Only warnings available, no actions | Recommendation insufficient; Warning may still fill |

---

# 10. Dependencies

| Depends on | Consumed by |
|------------|-------------|
| Interpretation + Evidence; Impact/Observation preferred | Executive Summary, Conclusion, Portal recommendation zone, Report CTA blocks |
| Must not wait for Warning | Warning is parallel concern after Recommendation in official order |

---

# 11. Extension Points

- Additional recommendation items under verbosity profiles  
- Domain-tagged recommendations (optional intents) with evidence  

No extension may create actions from score numbers alone without Interpretation/Evidence action support policy defined in a later content sprint.

---

# 12. Quality Rules

| Question | Answer |
|----------|--------|
| What information is required? | Action-supporting Interpretation/Evidence |
| Why does this component exist? | Convert meaning into prioritized guidance |
| When should it appear? | After Impact in official flow |
| When should it be omitted? | Never silently; Insufficient Evidence if no support |
| What should consume its output? | Executive Summary, Portal recommendations, Conclusion, Report |

---

# 13. Anti-patterns

✗ Generating template phrases in this grammar doc  
✗ “Always advise X” without evidence  
✗ Duplicating Warning text as a recommendation  
✗ Re-ranking via a new Narrative scoring system  
✗ Repeating full Interpretation counsel blocks without structural reorganization  

---

END
