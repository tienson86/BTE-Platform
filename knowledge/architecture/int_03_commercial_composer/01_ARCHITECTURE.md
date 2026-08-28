# 01 — Architecture

| Field | Value |
|-------|--------|
| Document | INT-03A Commercial Composer Architecture |
| Version | 1.0.0 |
| Status | Canonical for INT-03A |

---

## 1. Purpose

Commercial Composer turns published Integrated Narrative into a customer-facing consulting reading.

It is not a scoring engine. It is not Pack 05. It is not an LLM.

---

## 2. Position

```
Engine Result (frozen)
        ↓
Topic Narrative Units (INT-02, frozen)
        ↓
IntegratedNarrativeUnit (INT-02F, frozen)
        ↓
Commercial Composer (INT-03)   ← this epic
        ↓
CommercialNarrativeUnit
        ↓
(later, only after freeze) Report / PDF / DOCX / Portal
```

Workspace remains an Integrated Narrative consumer.

Pack 05 `NarrativeResult` remains the existing Report commercial contract until a later consume sprint.

---

## 3. Responsibilities

The Commercial Composer owns:

- commercial section inventory and order
- mapping from Integrated blocks to commercial sections
- merge / rewrite / simplify / reorder / summarize of **already published** sentences
- traceability from each commercial sentence to Integrated blocks

The Commercial Composer does **not** own:

- calendar conversion
- chart construction
- strength / pattern / useful-god / luck calculation
- identity assembly
- Integrated Narrative composition
- workspace layout
- report / PDF / DOCX rendering
- LLM rewrite

---

## 4. Input / output

| Direction | Type |
|-----------|------|
| Input | `IntegratedNarrativeUnit` (or its published dict) |
| Output | `CommercialNarrativeUnit` |

If Integrated Narrative is absent or insufficient, every commercial section uses `Chưa có dữ liệu`.

Do not rebuild from Strength, Useful God, Pattern, or Luck topic units.

---

## 5. Faithfulness

Every commercial sentence must be an Integrated sentence, or a summary built only from Integrated sentences.

No new analytical facts.

No predicted outcomes.

No invented domains (career / finance / health) unless those words already exist in Integrated Narrative.

---

END
