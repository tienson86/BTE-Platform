# causes / families

| Field | Value |
|-------|-------|
| Pack | PACK_01_STRENGTH |
| Topic | causes |
| File | families |
| Status | Draft |

Each heading is one Knowledge Unit. Schema: CATALOG_SCHEMA.md.

---
## IK-STR-CAUS-0001

| Field | Value |
|-------|-------|
| knowledge_id | IK-STR-CAUS-0001 |
| title | A cause is how the chart feeds, holds, empties, or presses |
| pack | PACK_01_STRENGTH |
| topic | causes |
| purpose | WHY |
| domain | strength_core |
| strength_class | all |
| customer_mode | ALLOWED |
| validation_mode | ALLOWED |
| required_facts | classification |
| optional_facts |  |
| forbidden_conditions |  |
| required_evidence | CLASS_ONLY |
| customer_value | HIGH |
| specificity | GENERIC |
| priority | CORE |
| duplicate_cluster | NONE |
| conflicts_with |  |
| reason_codes | SELECTED_CAUSE_PRESENT, REJECTED_MISSING_EVIDENCE, REJECTED_FACT_INACTIVE, REJECTED_INSUFFICIENT_EVIDENCE, REJECTED_CLASS_MISMATCH, REJECTED_NOT_APPLICABLE, MERGED_CAUSE_SPECIAL_INTO_SEASON, CONFLICT_QUALIFY, DEFERRED_TO_VALIDATION |
| narrative_weight | SUPPORTING |
| version | 1.0.0 |
| status | Draft |
| source_document | 02_CAUSES.md |

**claim**

The class is not a mood. It is the net of season, root, support, drain, control, and combination/clash/void as lived weather.

**supporting_points**

- Season: the climate of birth feeds you — or does not.
- Root: you have ground to stand on — or you float.
- Support: backup of the same nature stands with you.
- Drain: effort leaves you faster than it returns.
- Control: something sits on you and limits free movement.
- Combination / clash / void: support is merged, shaken, or emptied.

**limitations**

- Do not narrate a cause the engine has not published.
- Do not give formulas, thresholds, or Rule IDs.
- Do not use this unit as a glossary dump in Customer Mode; use only present causes.

---
## IK-STR-CAUS-0025

| Field | Value |
|-------|-------|
| knowledge_id | IK-STR-CAUS-0025 |
| title | Customer Why — only present weather |
| pack | PACK_01_STRENGTH |
| topic | causes |
| purpose | WHY |
| domain | strength_core |
| strength_class | all |
| customer_mode | FORBIDDEN |
| validation_mode | ALLOWED |
| required_facts | classification |
| optional_facts |  |
| forbidden_conditions |  |
| required_evidence | CLASS_ONLY |
| customer_value | LOW |
| specificity | GENERIC |
| priority | OPTIONAL |
| duplicate_cluster | NONE |
| conflicts_with |  |
| reason_codes | SELECTED_CAUSE_PRESENT, REJECTED_MISSING_EVIDENCE, REJECTED_FACT_INACTIVE, REJECTED_INSUFFICIENT_EVIDENCE, REJECTED_CLASS_MISMATCH, REJECTED_NOT_APPLICABLE, MERGED_CAUSE_SPECIAL_INTO_SEASON, CONFLICT_QUALIFY, DEFERRED_TO_VALIDATION |
| narrative_weight | OPTIONAL |
| version | 1.0.0 |
| status | Draft |
| source_document | 02_CAUSES.md |

**claim**

When Cause knowledge is composed into Customer Mode Why, keep only the causes that are present, in human weather: not standing alone; standing alone; effort leaks; something sits on you; the floor moves. That is enough. The rest is Validation Mode.

**supporting_points**

(empty — source gives a single atomic claim)

**limitations**

- This is a composition rule, not a Customer headline.
- Do not print this paragraph to the customer.

---
