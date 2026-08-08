# 12_NARRATIVE_FLOW_SPEC.md

Version: 1.0

Status: DRAFT — Sprint B Grammar

Pack: 05 (Narrative Engine)

Document: Narrative Flow Specification

Depends on: Sprint A (frozen) + Components 05–11

---

# 1. Purpose

This document defines **how Narrative components are ordered and combined**.

It specifies grammar of flow only.

It does not specify sentence text, templates, or generation algorithms.

---

# 2. Architectural Invariants (Flow-Level)

| Invariant | Rule |
|-----------|------|
| Not an inference engine | Flow never creates new analytical meaning |
| Not a rule engine | Flow never matches scoring rules |
| Not a scoring engine | Flow never alters grades/scores |
| Reorganization only | Flow reorganizes validated Interpretation into commercial structure |
| Meaning lock | Analytical meaning remains unchanged |
| Insufficient Evidence | Any component lacking support emits explicit Insufficient Evidence state |

---

# 3. Official Flow (Required Order)

```
Executive Summary
    ↓
Observation
    ↓
Reasoning
    ↓
Impact
    ↓
Recommendation
    ↓
Warning
    ↓
Conclusion
```

This is the **canonical commercial reading order**.

Portal / Report may visually emphasize Executive Summary first; body order follows this sequence.

---

# 4. Component Index in Flow

| Order | Component | Spec | Shell mandatory | Content may be Insufficient Evidence |
|------:|-----------|------|-----------------|--------------------------------------|
| 0 | Executive Summary | `05_EXECUTIVE_SUMMARY_SPEC.md` | Yes | Yes (per slot) |
| 1 | Observation | `06_OBSERVATION_COMPONENT.md` | Yes | Yes |
| 2 | Reasoning | `07_REASONING_COMPONENT.md` | Yes | Yes |
| 3 | Impact | `08_IMPACT_COMPONENT.md` | Yes | Yes |
| 4 | Recommendation | `09_RECOMMENDATION_COMPONENT.md` | Yes | Yes |
| 5 | Warning | `10_WARNING_COMPONENT.md` | Yes | Yes |
| 6 | Conclusion | `11_CONCLUSION_COMPONENT.md` | Yes | Yes |

---

# 5. Required Order Rules

1. Executive Summary is always first in the published narrative package.  
2. Observation precedes Reasoning.  
3. Reasoning precedes Impact.  
4. Impact precedes Recommendation.  
5. Recommendation precedes Warning in the official body order.  
6. Conclusion is always last.  
7. No component may leapfrog another in the published order.  

---

# 6. Optional Order

Optional **sub-intents** (future content packs) may appear **inside** a parent component’s structural slots, not as new positions that break the official seven.

Examples of optional *extensions* (not new official positions):

- Optional theme facets under Observation / Impact  
- Additional recommendation items under Recommendation  

Optional extensions:

- Must not reorder the seven official components  
- Must not appear before their parent component’s prerequisites are satisfied  
- Must emit Insufficient Evidence rather than invent content  

---

# 7. Conditional Order

Conditional rules affect **fill state**, not published sequence.

| Condition | Flow effect |
|-----------|-------------|
| Observation = Insufficient Evidence | Reasoning + Impact must be Insufficient Evidence |
| Reasoning = Insufficient Evidence | Impact may still fill **only if** Interpretation provides implication units tied directly to Observation evidence (preferred path still Reasoning→Impact) |
| Impact = Insufficient Evidence | Recommendation / Warning may still fill from direct action/caution evidence |
| Recommendation = Insufficient Evidence | Warning / Conclusion may still fill |
| Warning = Insufficient Evidence | Conclusion may still close from other filled components |
| All body components Insufficient Evidence | Executive Summary slots mostly insufficient; Conclusion insufficient; NarrativeResult status = `partial_insufficient` |

**Conditional build sequencing (internal):**

Executive Summary may be **finalized last** after body components, while remaining **first in published order**.

```
Build (internal, allowed):
  Observation → Reasoning → Impact → Recommendation → Warning → Conclusion
  → finalize Executive Summary

Publish (external, required):
  Executive Summary → Observation → … → Conclusion
```

---

# 8. Dependencies Diagram

```
                    Interpretation (validated)
                              │
                              ▼
                         EvidenceSet
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
 Observation ──► Reasoning ──► Impact ──► Recommendation
        │                         │              │
        │                         │              ▼
        │                         └────────► Warning
        │                                        │
        └────────────────► Conclusion ◄──────────┘
                              ▲
                              │
                      Executive Summary
                   (publishes first; may finalize last)
```

---

# 9. Failure Rules

| Failure | Flow response |
|---------|---------------|
| Invalid / missing Interpretation | Abort narrative compose — Public API error |
| Valid Interpretation, sparse evidence | Continue; mark Insufficient Evidence per component/slot |
| Component emits content without evidence_refs | Invalid NarrativeResult — reject at validation |
| Component invents conclusion | Forbidden — validation failure |
| Order violation in output | Invalid NarrativeResult — reject |
| Executive Summary contradicts Conclusion | Invalid — must reconcile structurally or mark insufficient, never invent |

---

# 10. Insufficient Evidence State (Flow Grammar)

Canonical state name: **`Insufficient Evidence`**

| Applies to | Behavior |
|------------|----------|
| Component | `insufficient_data = true`; shell remains in order |
| Executive slot | Slot flag in `insufficient_flags` |
| Downstream | Dependents follow conditional rules in §7 |
| Portal / Report | Consume state explicitly; do not invent fill |

Sprint B does not define customer-facing sentence strings for this state (platform copy is owned elsewhere). Grammar only requires the state to exist and propagate correctly.

---

# 11. What Consumes the Flow

| Consumer | Uses |
|----------|------|
| NarrativeResult | Stores components in official order |
| Portal Adapter | Maps Executive Summary + body components to Result zones |
| Report Engine | Renders narrative package in official order |
| API narrative view | Serializes ordered components |

---

# 12. Quality Rules (Flow)

| Question | Answer |
|----------|--------|
| What information is required? | Validated Interpretation + EvidenceSet; seven component shells |
| Why does this flow exist? | Guarantee coherent commercial reading without analytical drift |
| When should the full flow appear? | Every successful Narrative compose |
| When should a step be omitted? | Never omit shells; only Insufficient Evidence content |
| What should consume the flow? | NarrativeResult → Portal / Report / API |

---

# 13. Anti-patterns (Flow)

✗ Publishing Recommendation before Observation  
✗ Skipping Reasoning silently when Observation is filled  
✗ Using Warning to replace Recommendation in order  
✗ Ending on Recommendation without Conclusion shell  
✗ Parallel “free-form” section dumps that bypass the seven-component grammar  
✗ Generating prose/templates/examples inside flow docs  
✗ Inferring new facts to “complete” the flow  

---

# 14. Mapping to Sprint A Pipeline

Sprint A pipeline stages still hold:

```
AnalysisResult → Evidence → Composer → Section Builder → Story Builder → NarrativeResult
```

Sprint B grammar defines **section intents / component order** that Composer plans and Section Builder emits:

| Flow component | Section intent (logical) |
|----------------|--------------------------|
| Executive Summary | `NarrativeSummary` (+ optional overview section) |
| Observation | `observation` |
| Reasoning | `reasoning` |
| Impact | `impact` |
| Recommendation | `recommendation` |
| Warning | `warning` |
| Conclusion | `conclusion` |

---

# 15. Sprint B Completion Checklist

| Component / Spec | Complete contract | Dependencies | Quality rules | Output spec |
|------------------|-------------------|--------------|---------------|-------------|
| Executive Summary | Yes | Yes | Yes | Yes |
| Observation | Yes | Yes | Yes | Yes |
| Reasoning | Yes | Yes | Yes | Yes |
| Impact | Yes | Yes | Yes | Yes |
| Recommendation | Yes | Yes | Yes | Yes |
| Warning | Yes | Yes | Yes | Yes |
| Conclusion | Yes | Yes | Yes | Yes |
| Narrative Flow | Yes | Yes | Yes | Yes |

---

# 16. Stop

Sprint B ends here.

No implementation.

No templates.

No NLG.

Ready for a later sprint only after grammar acceptance.

---

END
