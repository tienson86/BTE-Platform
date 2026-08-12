# Output Specification — PACK-01 Prototype

| Field | Value |
|-------|-------|
| Document | OUTPUT_SPECIFICATION |
| Pack | PACK-01 Prototype |
| Version | 1.0.0 |

---

# 1. Purpose

Logical contract of `DualModeInterpretation` for Strength.

Not a production schema file.

Not a report layout.

---

# 2. Aggregate

```text
DualModeInterpretation
├── meta
│   ├── pack            PACK-01
│   ├── domain          strength
│   ├── prototype_version 1.0.0
│   ├── case_id         (example: CASE-0001)
│   └── locale
├── input_facts_ref     (hash / list of S0 fields used)
├── evidence            Evidence Layer
├── selection
│   ├── selected[]
│   ├── rejected[]      {unit_id, reason}
│   ├── duplicates_dropped[]
│   └── conflicts_applied[]
├── validation          Mode A
└── customer            Mode B
```

Determinism: same `input_facts_ref` → same aggregate.

---

# 3. Mode A object

```text
validation
├── final_conclusion    {id, label_en, label_vi, source}
├── evidence            groups[]
├── rule_trace          items[]
├── confidence          {engine_input, interpretation_pct, band, why}
├── alternative         {primary, runner_up | none_plausible, why}
├── missing_data        fields[]
└── conflicts           items[] | none
```

---

# 4. Mode B object

```text
customer
├── conclusion
├── why
├── meaning
├── advantages
├── challenges
├── life_influence
│   ├── personality?    (if units survived)
│   ├── career
│   ├── wealth
│   ├── marriage
│   ├── health
│   ├── learning?
│   ├── leadership?
│   └── decision_making?
├── luck                content | insufficient_data
├── recommendations     {do[], avoid[]}
└── executive_summary   5..8 lines
```

Each text node:

```text
{ text, unit_ids[], evidence_ids[], job, why_paragraph_exists }
```

`unit_ids` / `evidence_ids` / `job` / `why_paragraph_exists` are stripped before any customer render.

---

# 5. Insufficient Data node

```text
{ state: insufficient_data, reason_code, customer_text }
```

`reason_code` is Mode A only.

`customer_text` is leak-free.

---

# 6. Non-goals

- HTML / PDF
- Portal ViewModel
- Sentence library IDs
- Production API payload

---

END
