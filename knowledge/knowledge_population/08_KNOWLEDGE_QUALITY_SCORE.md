# 08 — Knowledge Quality Score

Version: 1.0  
Status: **OFFICIAL — Quality Scoring Framework**  
Date: 2026-08-08  
Depends on: `06_GOLDEN_KNOWLEDGE_STANDARD.md`  
Scope: Documentation only  

---

## 1. Purpose

Define the official **0–10 scoring framework** for Knowledge Units.

Scores support:

- Golden designation  
- Publish vs revision decisions  
- Wave-over-wave quality tracking  

---

## 2. Score categories

| # | Category | What it measures |
|---|----------|------------------|
| 1 | Accuracy | Correctness vs Analysis meaning |
| 2 | Evidence Quality | Conditions, required evidence, bindable placeholders |
| 3 | Commercial Value | Consultation impact |
| 4 | Actionability | Specificity of counsel / posture |
| 5 | Narrative Support | Fit to Pack 05 slots & CQ shape |
| 6 | Readability | Natural professional VI |
| 7 | Consistency | Aligns with sibling units & models |
| 8 | Reusability | Multi-scenario / multi-channel |
| 9 | Traceability | Ids, refs, version, pairs |
| 10 | Maintainability | Future-proof, clear notes, versionable |

Each category: **0–10 integer** (reviewers may use .5 only if team adopts half-scores later; default integers).

**Total score** = sum of 10 categories → **0–100**.

---

## 3. Per-category rubric (summary)

| Score | Meaning |
|------:|---------|
| 0–2 | Fail / missing / harmful |
| 3–4 | Weak; major revision |
| 5–6 | Acceptable baseline |
| 7–8 | Strong |
| 9–10 | Exemplary / Golden-grade |

### Anchors

| Category | 10 looks like | 3 looks like |
|----------|---------------|--------------|
| Accuracy | Conditions + body perfectly aligned | Advises against signal |
| Evidence Quality | Tight conditions + complete bind contract | Always-on fluff |
| Commercial Value | Clearly lifts Exec/Rec | Nice but unused trivia |
| Actionability | Concrete next step / clear framing | Vague slogan |
| Narrative Support | Slot-perfect CQ shape | Wrong evidence kind |
| Readability | Natural consultant VI | Jargon / stiff |
| Consistency | Harmonizes with pack | Conflicts sibling units |
| Reusability | Many scenarios/channels | One-off blob |
| Traceability | Full refs + version + pairs | Missing ids/refs |
| Maintainability | Clear notes; easy revise | Brittle / opaque |

---

## 4. Score interpretation (total 0–100)

| Total | Band | Meaning |
|------:|------|---------|
| 90–100 | **Golden** | Golden Reference eligible |
| 80–89 | **Strong** | Publish-eligible; minor polish optional |
| 70–79 | **Acceptable** | Publish-eligible if no HF; improve next revise |
| 60–69 | **Revision zone** | REVISION REQUIRED before Publish |
| 0–59 | **Reject / major rewrite** | Do not Approve |

---

## 5. Official thresholds

| Threshold | Rule |
|-----------|------|
| **Golden threshold** | Total ≥ **90** AND no category &lt; 7 AND all Golden criteria Pass |
| **Publish threshold** | Total ≥ **70** AND no category &lt; 5 AND no Hard Fail (`03`) AND all reviews Pass including Product |
| **Revision threshold** | Total &lt; **70** OR any category ≤ 4 OR any Hard Fail OR any Golden criterion Fail marked blocking |

### Special rules

| Rule | Detail |
|------|--------|
| Ethics/safety fail | Automatic Revision/Reject regardless of total |
| Risk without Mitigation (RK kind) | Cap Narrative Support at 4 until paired |
| Missing evidence_kind | Cap Evidence Quality and Narrative Support at 2 |

---

## 6. Scoring process

1. Each reviewer scores categories in their lens (Tech→Evidence/Trace/Maintain; Knowledge→Accuracy/Explainability via Readability+Accuracy; Commercial→Value/Action; Narrative→Narrative/Readability; Product→Value/Consistency).  
2. Wave lead consolidates to one official scorecard per unit.  
3. Disputes &gt;2 points on a category → escalate Architect.  
4. Record scorecard with unit version in review packet.

---

## 7. Scorecard template

```text
knowledge_unit_id:
version:
wave_id:
Accuracy: /10
Evidence Quality: /10
Commercial Value: /10
Actionability: /10
Narrative Support: /10
Readability: /10
Consistency: /10
Reusability: /10
Traceability: /10
Maintainability: /10
TOTAL: /100
Band:
Decision hint: Golden / Publish / Revision / Reject
Notes:
```

---

## 8. Stop line

Quality score framework finalized.  
Applied to Wave 1.1 in `09` / `10` without modifying units.

---

END
