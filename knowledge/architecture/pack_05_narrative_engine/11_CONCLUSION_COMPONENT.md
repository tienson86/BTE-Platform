# 11_CONCLUSION_COMPONENT.md

Version: 1.0

Status: DRAFT — Sprint B Grammar

Pack: 05 (Narrative Engine)

Component: Conclusion

Depends on: Sprint A (frozen)

---

# 1. Purpose

Conclusion **closes** the commercial narrative by consolidating already-established components.

It answers: “What is the closing takeaway?”

It does not introduce new analytical findings.

---

# 2. Responsibilities

Conclusion **must**

✓ Synthesize Observation → Recommendation/Warning into a closing structure  
✓ Remain within meanings already present upstream  
✓ Align with Executive Summary (no contradictory close)  
✓ Mark Insufficient Evidence when nothing valid can be concluded  

Conclusion **must not**

✗ Add new facts or scores  
✗ Re-open Reasoning with new causes  
✗ Override Recommendation / Warning with new advice  
✗ Invent a happier or harsher ending than sources allow  

---

# 3. Inputs

| Input | Required | Role |
|-------|----------|------|
| Observation | Preferred | Closing anchor |
| Impact | Preferred | Meaning close |
| Recommendation | Preferred | Action close |
| Warning | Preferred | Caution close |
| Executive Summary | Preferred | Consistency check |
| Validated Interpretation (closing / summary units) | Optional support | Closing meaning |
| EvidenceSet | **Yes** | Trace + sufficiency |

---

# 4. Required Evidence

| Condition | Rule |
|-----------|------|
| At least one upstream filled component | Required for a filled Conclusion |
| Closing Interpretation unit | Optional; not required if synthesis of upstream components is possible structurally |
| If all upstream required bodies are Insufficient Evidence | Conclusion = Insufficient Evidence |

Conclusion evidence_refs should union upstream refs used in the close — not new analytical sources.

---

# 5. Required Interpretation

| Requirement | Rule |
|-------------|------|
| No new Interpretation claims | Conclusion may use closing units only if they do not add unseen conclusions |
| Consistency with Executive Summary | Required |
| Commercial suitability | Technical prose excluded |

---

# 6. Output Contract

Logical section intent: `conclusion`

| Field | Rule |
|-------|------|
| `intent` | `conclusion` |
| `paragraphs[].role` | Primarily `summary` |
| `depends_on` | Upstream component ids |
| `evidence_refs` | Union of supporting upstream refs |
| `insufficient_data` | True when no closable content |
| `recommendations` | Must not introduce new recommendation items; may reference existing ones structurally |

---

# 7. Narrative Position

```
Executive Summary
Observation
Reasoning
Impact
Recommendation
Warning
[Conclusion]   ← position 6 (last)
```

Always last in the official flow.

---

# 8. Priority

| Priority | Value |
|----------|-------|
| Flow priority | **P1 — Required closing shell** |
| Omission | Never omit shell; Insufficient Evidence if nothing to close |

---

# 9. Failure Handling

| Condition | Handling |
|-----------|----------|
| No filled upstream narrative bodies | Conclusion insufficient |
| Upstream contradiction unresolved | Do not invent resolution; insufficient or limited close using non-conflicting subset |
| Closing Interpretation adds new claims | Reject those units |

---

# 10. Dependencies

| Depends on | Consumed by |
|------------|-------------|
| Full prior flow (structurally) | Report closing section, Portal closing card, NarrativeResult tail |
| Executive Summary | Bidirectional consistency — Conclusion must not fight Summary |

---

# 11. Extension Points

- Optional epilogue themes only with explicit evidence  
- Verbosity controlling close length — not new meaning  

---

# 12. Quality Rules

| Question | Answer |
|----------|--------|
| What information is required? | At least one valid upstream narrative body or closing Interpretation unit without new claims |
| Why does this component exist? | Provide a coherent ending without new analysis |
| When should it appear? | Always last |
| When should it be omitted? | Never silently; Insufficient Evidence if empty |
| What should consume its output? | Report close, Portal close, API narrative tail |

---

# 13. Anti-patterns

✗ Surprising new conclusions in the last section  
✗ Re-scoring “final grade narrative” beyond Score output already narrated  
✗ Copying Executive Summary verbatim without structural close role  
✗ Generating inspirational prose assets in this grammar sprint  
✗ Using Conclusion to hide Insufficient Evidence from earlier components  

---

END
