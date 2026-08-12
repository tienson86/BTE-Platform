# NarrativePlan

| Field | Value |
|-------|-------|
| Document | NARRATIVE_PLAN |
| Version | 1.0.0 |

---

# 1. Purpose

The Reasoning Engine’s primary output is **`NarrativePlan`**, not sentences.

Sentence Composer consumes the plan.

---

# 2. Schema

```text
NarrativePlan
├── meta
│   ├── subject
│   ├── versions (schema, policy, knowledge, standard)
│   └── case_id
├── primary_conclusion
│   ├── class_id
│   ├── language_strength          firm | qualified | cautious
│   └── unit_ids[]                 usually empty or CONCLUSION pointer
├── reasoning_chain[]
├── sections[]
│   ├── section_id
│   ├── purpose
│   ├── intent
│   ├── selected_units[]
│   ├── rejected_units[]           with reason_code (also in diagnostics)
│   ├── narrative_priority
│   ├── language_strength
│   ├── transition_requirement     intent enum, not wording
│   └── insufficient_data          bool + reason_code
├── warnings[]
├── omitted_domains[]
├── missing_data[]
├── alternative                    Validation payload; customer_qualifier optional
├── executive_summary_plan         see EXECUTIVE_SUMMARY_PLANNING
└── diagnostics
    ├── candidates[]
    ├── gate_results[]
    ├── relevance[]
    ├── salience[]
    ├── duplicate_clusters[]
    ├── conflicts[]
    ├── ranks[]
    └── claim_traces[]
```

`diagnostics` = Mode A / Validation.

Customer render uses `sections`, `warnings` (leak-free), `executive_summary_plan`, `primary_conclusion`.

---

# 3. Section intents (closed)

```text
NAME_STANDING
EXPLAIN_CAUSES
STATE_MEANING
LIST_ADVANTAGES
LIST_CHALLENGES
DOMAIN_IMPLICATION
LUCK_INTERACTION
LUCK_INSUFFICIENT
ADVISE
WARN
SUMMARIZE
```

---

# 4. language_strength

| Value | When |
|-------|------|
| `firm` | high/canonical confidence, no live class alternative needed |
| `qualified` | medium, or C1 live, or thin-root qualifier |
| `cautious` | low, or borderline alternative, or partial evidence |

Composer maps these to modality. Customer never sees the enum name.

---

# 5. Determinism

Same `ReasoningInput` + versions → same `NarrativePlan` byte-stable canonical serialization.

---

END
