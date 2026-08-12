# Knowledge Unit Metadata

| Field | Value |
|-------|-------|
| Document | KNOWLEDGE_UNIT_METADATA |
| Pack | PACK-01 Strength |
| Version | 1.0.0 |

---

# 1. Purpose

Metadata the Reasoning Engine needs to decide keep / drop / qualify / hide.

This is a **design contract** for future knowledge records.

This pack does not rewrite `knowledge/interpretation_knowledge/` in this task.

---

# 2. Required fields

| Field | Type | Meaning |
|-------|------|---------|
| `knowledge_id` | ID | Stable, e.g. `IK-STR-MEAN-ST-01` |
| `pack` | enum | `PACK_01_STRENGTH` |
| `topic` | string | File/topic key (meanings, causes, …) |
| `strength_class` | enum | `very_strong` `strong` `balanced` `weak` `very_weak` `all` `edge` |
| `domain` | enum | See §4 |
| `purpose` | enum | See §3 |
| `claims[]` | list | Atomic claims the unit is allowed to make |
| `required_facts[]` | list | Fact dimensions that must be AVAILABLE |
| `optional_facts[]` | list | Improve relevance if present |
| `forbidden_conditions[]` | list | If true → ineligible |
| `priority` | int 1–100 | **Knowledge** priority (not rule, not narrative) |
| `severity` | enum | `info` `consideration` `caution` `warning` |
| `customer_value` | enum | `low` `medium` `high` `critical` |
| `specificity` | enum | `generic` `class_level` `cause_specific` `case_specific` |
| `confidence_requirement` | enum | `any` `medium_plus` `high_plus` |
| `dependencies[]` | ids | Other units that should exist in the plan if this is kept |
| `conflicts_with[]` | ids or claim keys | Potential knowledge conflicts |
| `duplicates[]` | ids or overlap keys | Known duplicate family |
| `mode_visibility` | enum | `customer` `validation` `both` |

---

# 3. Purpose taxonomy (closed)

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

One purpose per unit.

A recommendation that is secretly a meaning fails metadata.

---

# 4. Domain taxonomy (closed)

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

No free-text domains.

`strength_core` = conclusion, why, meaning, core advantage/challenge not yet specialized to a life domain.

---

# 5. Enum definitions

**severity**

| Value | Use |
|-------|-----|
| `info` | Neutral elaboration |
| `consideration` | Worth noticing |
| `caution` | Operating cost |
| `warning` | Risk that needs a WARNING purpose or rec avoid |

**customer_value**

How much a paying customer can **use** the claim, not how classical it is.

**specificity**

`generic` (“strong people persist”) loses to `cause_specific` (“thin root + control”) when both eligible.

**confidence_requirement**

If interpretation confidence band is below the requirement, unit is Validation-only or dropped from Customer Mode.

**mode_visibility**

`validation` = never Customer Mode even if salient (e.g. alternative shares).

---

# 6. Claims

Each claim:

```text
claim_id
proposition          one idea
polarity             support | cost | action | qualify
absolute             true/false  (true is almost always forbidden for advice)
```

Advice claims with `absolute = true` fail Advice Safety (see Conflict / Advice constraints in CONFLICT_REASONING and this pack’s safety rule: tendency only).

---

# 7. Forbidden conditions (examples)

```text
drain_inactive
root_thin
luck_missing
class_not_strong
special_is_not_override
```

CASE-0001: `root_deep` units carry `forbidden_conditions: [root_thin]` or required_facts deep root.

---

END
