# Knowledge Catalog Schema — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | KNOWLEDGE_CATALOG |
| Status | FROZEN |
| Form | Architecture only — not JSON, not code |

---

# 1. Purpose

Interpretation Knowledge files contain **prose knowledge**.

The catalog is the **deterministic record** the Reasoning Engine may read.

One Knowledge Unit = one catalog row.

Prose files are not deleted. Catalog **points at** them.

This freeze does not populate every row. It freezes **the schema** every row must obey.

---

# 2. Schema — every field

| Field | Closed values / type | Meaning |
|-------|----------------------|---------|
| `knowledge_id` | `IK-STR-<TOPIC>-<CLASS>-<NN>` | Stable identity. Never reused after deprecation. |
| `pack` | `PACK_01_STRENGTH` | Owning pack. |
| `topic` | `meanings` `causes` `advantages` `challenges` `personality` `career` `wealth` `marriage` `health` `luck` `recommendations` `edge` `examples` | Source chapter. |
| `purpose` | See §3 | Narrative job. One purpose per unit. |
| `domain` | See §4 | Life/core domain. Not free text. |
| `strength_class` | `very_strong` `strong` `balanced` `weak` `very_weak` `all` `edge` | Class gate. |
| `required_facts` | list of fact keys | All must be in an allowed evidence state (usually AVAILABLE). |
| `optional_facts` | list of fact keys | If present, raise relevance/salience; absence does not fail the gate. |
| `forbidden_conditions` | list of condition keys | If any true → ineligible. |
| `evidence_requirement` | `full` `partial_ok` `class_only` | How strict the gate is. |
| `customer_value` | `low` `medium` `high` `critical` | Usefulness to a paying customer, not classical prestige. |
| `priority` | integer 1–100 | **Knowledge** priority (tie-break only). Not rule priority. Not narrative order. |
| `specificity` | `generic` `class_level` `cause_specific` `case_specific` | How tightly bound to this chart’s weather. |
| `dependencies` | list of `knowledge_id` | If this unit is kept, these should already be in the plan or the unit drops (`REJECTED_NO_CHAIN` for recs). |
| `conflicts` | list of `knowledge_id` or conflict keys | Declared knowledge conflicts. |
| `duplicate_cluster` | cluster id or `none` | Declared family. Runtime must not invent clusters. |
| `narrative_weight` | `required_shell` `primary` `supporting` `omit_ok` | Budget preference inside a section. |
| `reason_codes` | list of allowed codes this unit may emit | Subset of frozen reason codes. |
| `mode_visibility` | `customer` `validation` `both` | Where the unit may appear. |
| `version` | `V#.#.#` | Unit version. |
| `authoring_status` | `draft` `review` `official` `deprecated` | Only `official` may enter Customer Mode. |

---

# 3. Purpose (frozen)

```text
CONCLUSION
WHY
MEANING
ADVANTAGE
CHALLENGE
PERSONALITY
CAREER
WEALTH
MARRIAGE
HEALTH
LEARNING
LEADERSHIP
DECISION_MAKING
LUCK
RECOMMENDATION
WARNING
SUMMARY
EDGE_QUALIFIER
```

`examples` topic → purpose not used in Customer Mode (`REJECTED_TEACHING_EXAMPLE`).

---

# 4. Domain (frozen)

```text
strength_core
personality
career
wealth
marriage
health
learning
leadership
decision_making
luck
recommendation
```

---

# 5. Fact keys (PACK-01)

```text
classification
season
root
root_thin
root_deep
support
drain
drain_active
control
special
special_override
combination
luck_interaction
hidden_stems
```

`classification` is the published Strength class, not a score.

---

# 6. Forbidden condition keys (PACK-01)

```text
class_mismatch
root_thin
root_deep_required
drain_inactive
luck_missing
special_is_not_override
teaching_only
```

---

# 7. evidence_requirement

| Value | Gate |
|-------|------|
| `full` | every required_fact AVAILABLE (or INACTIVE only if the unit is *about* inactivity — PACK-01 has no such customer unit) |
| `partial_ok` | PARTIAL allowed; Customer Mode may not treat as firm |
| `class_only` | only `classification` required |

---

# 8. narrative_weight

| Value | Budget behavior |
|-------|-----------------|
| `required_shell` | never cut (Conclusion) |
| `primary` | cut last |
| `supporting` | cut first inside the section |
| `omit_ok` | may be omitted even under budget |

---

# 9. What this freeze does not do

- Does not rewrite `knowledge/interpretation_knowledge/PACK_01_STRENGTH/*.md`
- Does not emit JSON
- Does not invent CASE-0001-only hard-coded sentences

Authoring later **fills rows** that conform to this schema. Filling rows is not a V1.0 freeze change to prose knowledge.

---

END
