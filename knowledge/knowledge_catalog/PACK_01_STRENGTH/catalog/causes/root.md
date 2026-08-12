# causes / root

| Field | Value |
|-------|-------|
| Pack | PACK_01_STRENGTH |
| Topic | causes |
| File | root |
| Status | Draft |

Each heading is one Knowledge Unit. Schema: CATALOG_SCHEMA.md.

---
## IK-STR-CAUS-0005

| Field | Value |
|-------|-------|
| knowledge_id | IK-STR-CAUS-0005 |
| title | Root present — identity has a floor |
| pack | PACK_01_STRENGTH |
| topic | causes |
| purpose | WHY |
| domain | strength_core |
| strength_class | all |
| customer_mode | ALLOWED |
| validation_mode | ALLOWED |
| required_facts | classification, root |
| optional_facts |  |
| forbidden_conditions | root_thin |
| required_evidence | FULL |
| customer_value | HIGH |
| specificity | CONTEXTUAL |
| priority | CORE |
| duplicate_cluster | NONE |
| conflicts_with |  |
| reason_codes | SELECTED_CAUSE_PRESENT, REJECTED_MISSING_EVIDENCE, REJECTED_FACT_INACTIVE, REJECTED_INSUFFICIENT_EVIDENCE, REJECTED_CLASS_MISMATCH, REJECTED_NOT_APPLICABLE, MERGED_CAUSE_SPECIAL_INTO_SEASON, CONFLICT_QUALIFY |
| narrative_weight | CORE |
| version | 1.0.0 |
| status | Draft |
| source_document | 02_CAUSES.md |

**claim**

With root, you can take a hit and still be someone. Recovery is possible: you can leave a job, a city, an argument, and still know who is walking away.

**supporting_points**

(empty — source gives a single atomic claim)

**limitations**

- Use when root is published as present and not the thin-root story.
- Do not use the deep-root-plus-surplus picture unless those facts are also present.

---
## IK-STR-CAUS-0006

| Field | Value |
|-------|-------|
| knowledge_id | IK-STR-CAUS-0006 |
| title | Root absent — talent has nowhere to sit |
| pack | PACK_01_STRENGTH |
| topic | causes |
| purpose | WHY |
| domain | strength_core |
| strength_class | all |
| customer_mode | ALLOWED |
| validation_mode | ALLOWED |
| required_facts | classification, root |
| optional_facts |  |
| forbidden_conditions |  |
| required_evidence | FULL |
| customer_value | HIGH |
| specificity | CONTEXTUAL |
| priority | CORE |
| duplicate_cluster | NONE |
| conflicts_with |  |
| reason_codes | SELECTED_CAUSE_PRESENT, REJECTED_MISSING_EVIDENCE, REJECTED_FACT_INACTIVE, REJECTED_INSUFFICIENT_EVIDENCE, REJECTED_CLASS_MISMATCH, REJECTED_NOT_APPLICABLE, MERGED_CAUSE_SPECIAL_INTO_SEASON, CONFLICT_QUALIFY |
| narrative_weight | CORE |
| version | 1.0.0 |
| status | Draft |
| source_document | 02_CAUSES.md |

**claim**

Without root, talent can still exist, but it has nowhere to sit. Praise feels good and does not last. Crisis feels like vanishing. This person needs places and people that act as ground — not more slogans about grit.

**supporting_points**

(empty — source gives a single atomic claim)

**limitations**

- Use only when root is published as absent, not when root is unpublished.
- Unpublished root is REJECTED_MISSING_EVIDENCE, not this story.
- Do not treat this as the same unit as thin root.

---
## IK-STR-CAUS-0007

| Field | Value |
|-------|-------|
| knowledge_id | IK-STR-CAUS-0007 |
| title | Thin root — the floor is close |
| pack | PACK_01_STRENGTH |
| topic | causes |
| purpose | WHY |
| domain | strength_core |
| strength_class | all |
| customer_mode | ALLOWED |
| validation_mode | ALLOWED |
| required_facts | classification, root_thin |
| optional_facts | drain |
| forbidden_conditions |  |
| required_evidence | FULL |
| customer_value | HIGH |
| specificity | CONTEXTUAL |
| priority | CORE |
| duplicate_cluster | NONE |
| conflicts_with |  |
| reason_codes | SELECTED_CAUSE_PRESENT, REJECTED_MISSING_EVIDENCE, REJECTED_FACT_INACTIVE, REJECTED_INSUFFICIENT_EVIDENCE, REJECTED_CLASS_MISMATCH, REJECTED_NOT_APPLICABLE, MERGED_CAUSE_SPECIAL_INTO_SEASON, CONFLICT_QUALIFY |
| narrative_weight | CORE |
| version | 1.0.0 |
| status | Draft |
| source_document | 02_CAUSES.md |

**claim**

Thin root means the floor is close: ground exists, but it does not feel like a deep place to sit.

**supporting_points**

(empty — source gives a single atomic claim)

**limitations**

- Use when root_thin is published.
- Do not upgrade to “no root”.
- Do not require drain; drain-plus-thin-root is a separate unit.
- Do not use CAUSE-ROOT-DEEP language.

---
## IK-STR-CAUS-0008

| Field | Value |
|-------|-------|
| knowledge_id | IK-STR-CAUS-0008 |
| title | Deep root plus surplus season — hard to empty |
| pack | PACK_01_STRENGTH |
| topic | causes |
| purpose | WHY |
| domain | strength_core |
| strength_class | very_strong |
| customer_mode | ALLOWED |
| validation_mode | ALLOWED |
| required_facts | classification, root_deep, season |
| optional_facts |  |
| forbidden_conditions |  |
| required_evidence | FULL |
| customer_value | HIGH |
| specificity | CONTEXTUAL |
| priority | HIGH |
| duplicate_cluster | NONE |
| conflicts_with |  |
| reason_codes | SELECTED_CAUSE_PRESENT, REJECTED_MISSING_EVIDENCE, REJECTED_FACT_INACTIVE, REJECTED_INSUFFICIENT_EVIDENCE, REJECTED_CLASS_MISMATCH, REJECTED_NOT_APPLICABLE, MERGED_CAUSE_SPECIAL_INTO_SEASON, CONFLICT_QUALIFY |
| narrative_weight | SUPPORTING |
| version | 1.0.0 |
| status | Draft |
| source_document | 02_CAUSES.md |

**claim**

Deep root plus surplus season is how Very Strong often feels from the inside: hard to empty.

**supporting_points**

(empty — source gives a single atomic claim)

**limitations**

- Do not use when published classification is not very_strong.
- Do not use to decide or upgrade the class.
- Do not dump Rule IDs, scores, or thresholds.
- Use only when both deep root and feeding season are published.
- Do not use on Strong merely because the tank feels full.

---
## IK-STR-CAUS-0009

| Field | Value |
|-------|-------|
| knowledge_id | IK-STR-CAUS-0009 |
| title | Thin root plus drain — Weak floor story |
| pack | PACK_01_STRENGTH |
| topic | causes |
| purpose | WHY |
| domain | strength_core |
| strength_class | weak |
| customer_mode | ALLOWED |
| validation_mode | ALLOWED |
| required_facts | classification, root_thin, drain |
| optional_facts |  |
| forbidden_conditions | drain_inactive |
| required_evidence | FULL |
| customer_value | HIGH |
| specificity | CONTEXTUAL |
| priority | HIGH |
| duplicate_cluster | NONE |
| conflicts_with |  |
| reason_codes | SELECTED_CAUSE_PRESENT, REJECTED_MISSING_EVIDENCE, REJECTED_FACT_INACTIVE, REJECTED_INSUFFICIENT_EVIDENCE, REJECTED_CLASS_MISMATCH, REJECTED_NOT_APPLICABLE, MERGED_CAUSE_SPECIAL_INTO_SEASON, CONFLICT_QUALIFY |
| narrative_weight | SUPPORTING |
| version | 1.0.0 |
| status | Draft |
| source_document | 02_CAUSES.md |

**claim**

Thin root plus drain is how Weak often feels: the floor is close, and output spends what little floor there is.

**supporting_points**

(empty — source gives a single atomic claim)

**limitations**

- Do not use when published classification is not weak.
- Do not use to decide or upgrade the class.
- Do not dump Rule IDs, scores, or thresholds.
- Do not use when drain is INACTIVE (REJECTED_FACT_INACTIVE).
- Do not use when drain is unpublished (REJECTED_MISSING_EVIDENCE).

---
