# 04 — Composition Rules

| Field | Value |
|-------|--------|
| Document | INT-03A Composition Rules |
| Version | 1.0.0 |
| Status | Canonical for INT-03A |

---

## 1. Official order

```
IntegratedNarrativeUnit (read-only)
        ↓
Read Integrated blocks
        ↓
Drop machine-only sentences (JSON / list dumps)
        ↓
Map onto seven commercial sections
        ↓
CommercialNarrativeUnit
```

---

## 2. Allowed operations

The composer may only:

| Operation | Meaning in INT-03A |
|-----------|--------------------|
| merge | Place sentences from more than one Integrated block into one commercial section |
| rewrite | Rephrase an Integrated sentence without adding facts (identity copy in INT-03A) |
| simplify | Omit machine-only dumps; keep customer prose |
| reorder | Follow commercial section order, not Integrated block order |
| summarize | Conclusion selects already-published first sentences |

---

## 3. Forbidden operations

The composer must never:

- predict
- calculate
- infer unpublished analytical truth
- invent facts, domains, persona, or advice
- expand analytical truth beyond Integrated Narrative
- call Calendar, Bazi, Strength, Pattern, Useful God, Luck, or Identity
- call Pack 05 / Report / PDF / DOCX
- use an LLM

---

## 4. Traceability

Every published commercial sentence records:

- `integrated_slots`
- `source_paths`
- `topic_ids` when Integrated published them

If a sentence cannot cite Integrated Narrative, it is not published.

---

## 5. Determinism

Same IntegratedNarrativeUnit → same CommercialNarrativeUnit.

No wall-clock. No random order. No LLM.

---

## 6. Fail-closed

Missing Integrated Narrative → all seven sections insufficient.

Never a silent empty string that looks like a finished commercial reading.

---

END
