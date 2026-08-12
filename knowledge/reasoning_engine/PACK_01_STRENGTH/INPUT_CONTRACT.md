# Input Contract — ReasoningInput

| Field | Value |
|-------|-------|
| Document | INPUT_CONTRACT |
| Pack | PACK-01 Strength |
| Version | 1.0.0 |

---

# 1. Purpose

Logical contract for what the Reasoning Engine may see.

No raw engine objects (`StrengthResult` class instances, matcher internals).

Facts are already published and normalized.

---

# 2. ReasoningInput

```text
ReasoningInput
├── meta
│   ├── case_id
│   ├── locale
│   ├── reasoning_schema_version
│   ├── reasoning_policy_version
│   ├── knowledge_version
│   └── standard_version
├── subject                         enum: strength | pattern | … (PACK-01 = strength)
├── classification
│   ├── class_id                    strong | weak | balanced | very_strong | very_weak | unmapped
│   ├── class_label_vi
│   ├── class_label_en
│   └── source                      published_engine_level
├── facts[]                         normalized published facts (no raw objects)
├── evidence[]                      Evidence Layer items
├── selected_knowledge_units[]      candidates from selector (may still fail the gate)
├── conflicts[]                     already detected fact/dimension conflicts
├── missing_data[]                  fields with availability state
├── confidence
│   ├── engine_confidence           optional input
│   ├── interpretation_confidence   0–100 if already computed upstream
│   └── band                        experimental|low|medium|high|canonical
├── alternative_analysis
│   ├── primary
│   ├── runner_up                   optional
│   └── shares                      optional percents — Validation only
├── context
│   ├── question_context            optional future: wealth | career | …
│   ├── verbosity                   default | short | full
│   └── audience                    customer | validation
└── diagnostics_in                  optional upstream notes (not customer)
```

---

# 3. Fact item

```text
Fact
├── fact_id
├── dimension                       season | root | support | drain | control | special | level | luck | …
├── status                          AVAILABLE | PARTIAL | MISSING | NOT_APPLICABLE
├── polarity                        support | weaken | neutral | override | classify | inactive
├── observed                        leak-safe meaning key + internal value (internal_only)
└── evidence_ids[]
```

PACK-01 does not require Pattern/Useful God/Temperature facts. If present in a wider payload, they are **ignored** unless `subject` is that pack.

---

# 4. Classification lock

`classification.class_id` is read-only for reasoning.

The engine may:

- qualify language
- keep an alternative in Validation Mode

The engine may not:

- write a new class
- average Strong and Balanced into a third class

---

# 5. Confidence field

`confidence.interpretation_confidence` is an input to language and mode split.

It is not a life-success probability.

It must not be copied into Customer Mode as a number.

---

# 6. Invalid input

| Condition | Result |
|-----------|--------|
| missing `subject` or `classification` | fail closed — no NarrativePlan |
| `class_id = unmapped` | plan with insufficient_data on class-dependent sections |
| empty `facts` and empty `evidence` | fail closed or conclusion-only insufficient |
| unit list contains unknown ids | those units ineligible; do not crash the rest if classification exists |

---

END
