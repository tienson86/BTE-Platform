# 16_PARAGRAPH_STRUCTURE.md

Version: 1.0

Status: DRAFT — Sprint C Writing System

Pack: 05 (Narrative Engine)

Depends on: Sprint A (frozen) · Sprint B (frozen) · `13`–`15`

---

# 1. Purpose

This document defines **paragraph-level structure** for BTE Narrative.

A paragraph is a structural writing unit mapped to Sprint B roles.

It is not a runtime template file.

---

# 2. Core Paragraph Rule

**One paragraph → one narrative role.**

Do not mix Observation + Recommendation in the same paragraph.

Do not mix Warning + Celebration in the same paragraph.

---

# 3. Canonical Paragraph Anatomy

Preferred order inside a body paragraph:

```
Lead statement (role-defining)
    ↓
Support (evidence-backed elaboration)
    ↓
Optional bridge (only if needed for next component)
```

| Part | Required | Notes |
|------|----------|-------|
| Lead | Yes | States the paragraph’s job |
| Support | Usually | Must not invent |
| Bridge | Optional | Must not smuggle next component’s full job |

Executive Summary slots may be shorter than full paragraphs (slot-sized units).

---

# 4. Paragraph by Component

| Component | Paragraph pattern |
|-----------|-------------------|
| Executive Summary | Slot units, not long essays |
| Observation | Lead fact → supporting visible details |
| Reasoning | Lead rationale → linked support |
| Impact | Lead consequence → grounded implication |
| Recommendation | Action head → reason → optional benefit |
| Warning | Caution head → risk support |
| Conclusion | Synthesis lead → close without new claims |

---

# 5. Length and Balance

| Guidance | Rule |
|----------|------|
| Default body paragraph | Compact (typically 2–4 sentences) |
| Avoid | One component with huge walls of text next to empty siblings |
| Verbosity profiles | May expand support sentences — not invent new roles |
| Empty | Prefer Insufficient Evidence over decorative padding |

---

# 6. Paragraph Sequencing Inside a Component

When a component has multiple paragraphs:

1. General → specific  
2. Higher-confidence / higher-priority first  
3. No contradiction across paragraphs  
4. No duplicate restatement of the same claim in different words without need  

---

# 7. Mapping to Models (Sprint A)

| Writing unit | Model field |
|--------------|-------------|
| Body paragraph | `NarrativeParagraph` |
| Recommendation item block | `NarrativeRecommendation` |
| Executive slot | `NarrativeSummary` fields |
| Component group | `NarrativeSection` |

Writing rules constrain content quality; models constrain structure.

---

# 8. Transitions Between Components

Transitions are structural, not literary decoration contests.

| From → To | Transition job |
|-----------|----------------|
| Observation → Reasoning | Move from what → why |
| Reasoning → Impact | Move from why → so what |
| Impact → Recommendation | Move from meaning → action |
| Recommendation → Warning | Separate do-this from watch-this |
| Warning → Conclusion | Settle the arc |

Do not write transition paragraphs that add new analysis.

---

# 9. Anti-patterns (Paragraph)

✗ Kitchen-sink paragraphs covering the whole chart  
✗ Padding paragraphs with no evidence  
✗ Copying entire Interpretation sections as one paragraph  
✗ Using Conclusion paragraphs to reopen Impact debates  
✗ Recommendation paragraphs that only restate Warning  

---

END
