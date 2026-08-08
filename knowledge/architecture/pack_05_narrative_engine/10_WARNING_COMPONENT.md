# 10_WARNING_COMPONENT.md

Version: 1.0

Status: DRAFT — Sprint B Grammar

Pack: 05 (Narrative Engine)

Component: Warning

Depends on: Sprint A (frozen)

---

# 1. Purpose

Warning states **cautions and risks** already validated in Interpretation / Evidence.

It answers: “What must be watched or avoided?”

It is distinct from Recommendation (what to do) and Impact (what it means).

---

# 2. Responsibilities

Warning **must**

✓ Structure caution / risk / unfavorable units from Interpretation/Evidence  
✓ Keep severity within source claims  
✓ Support Executive Summary weakness slot when appropriate  
✓ Emit Insufficient Evidence when no caution support exists  

Warning **must not**

✗ Invent risks  
✗ Convert every weakness into catastrophic language beyond source  
✗ Replace Recommendation  
✗ Re-score unfavorable factors  

---

# 3. Inputs

| Input | Required | Role |
|-------|----------|------|
| Observation / Impact | Preferred | Context |
| Validated Interpretation (risk / caution / unfavorable units) | **Yes** for filled Warning | Caution meaning |
| EvidenceSet (weakness / risk / unfavorable gods / attention) | **Yes** | Sufficiency + tracing |

---

# 4. Required Evidence

Filled Warning requires at least one of:

| Evidence kind | Role |
|---------------|------|
| Weakness / risk | Primary |
| Unfavorable / kỵ signals | Primary |
| Attention / caution Interpretation units | Primary |

If none → Warning = **Insufficient Evidence** (component shell still allowed).

---

# 5. Required Interpretation

| Requirement | Rule |
|-------------|------|
| Caution units present for filled Warning | Required |
| No amplification beyond Interpretation | Severity lock |
| Commercial suitability | Exclude technical rule prose |

---

# 6. Output Contract

Logical section intent: `warning`

| Field | Rule |
|-------|------|
| `intent` | `warning` |
| `paragraphs[].role` | Caution-oriented structural role (e.g. observation of risk — not recommendation) |
| `evidence_refs` | Required when filled |
| `insufficient_data` | True when no caution evidence |
| `recommendations` | **Empty** (actions belong to Recommendation) |

Warnings may feed Executive Summary `weaknesses` but must not silently become `next_action`.

---

# 7. Narrative Position

```
Executive Summary
Observation
Reasoning
Impact
Recommendation
[Warning]   ← position 5
Conclusion
```

---

# 8. Priority

| Priority | Value |
|----------|-------|
| Flow priority | **P1 — Required shell** in official flow |
| Content | May be Insufficient Evidence without failing entire narrative |
| Relative to Recommendation | Official order places Warning after Recommendation; both may exist |

---

# 9. Failure Handling

| Condition | Handling |
|-----------|----------|
| No caution evidence | Insufficient Evidence |
| Caution contradicts Observation | Prefer AnalysisResult; drop unsupported caution unit |
| Only actions, no cautions | Warning insufficient; Recommendation may still fill |

---

# 10. Dependencies

| Depends on | Consumed by |
|------------|-------------|
| Interpretation + Evidence; Observation/Impact preferred | Executive Summary weaknesses, Conclusion, Portal caution blocks |
| Independent of Recommendation content | Must not require Recommendation to exist as filled |

---

# 11. Extension Points

- Severity metadata bands derived from source only  
- Optional domain warnings with evidence  

---

# 12. Quality Rules

| Question | Answer |
|----------|--------|
| What information is required? | Risk/caution Interpretation or Evidence |
| Why does this component exist? | Separate “watch outs” from “do this” |
| When should it appear? | After Recommendation in official flow |
| When should it be omitted? | Never silently; Insufficient Evidence if empty |
| What should consume its output? | Executive Summary, Conclusion, Portal warnings, Report attention blocks |

---

# 13. Anti-patterns

✗ Turning Warning into Recommendation  
✗ Inventing risks from missing data  
✗ Duplicating Impact text under a warning label  
✗ Using Warning to change analytical grade meaning  
✗ Repeating unfavorable Evidence lists without narrative reorganization structure  

---

END
