# Rule Specification

**Standard:** Knowledge Module Standard (KMS)  
**Version:** V1.0.0  
**Status:** Frozen (Rule Asset Standard)

---

# 1. Purpose

This document defines the mandatory specification for Rule Database assets and closely related rule-oriented assets.

---

# 2. Applicability

Applies when a Knowledge Module declares any of:

- Rule Database
- Decision Tables used as rule logic
- Priority Tables used for rule conflict ordering
- Formula Library entries consumed as rule effects

Does not redefine Terminology, Examples, or Report-oriented assets.

---

# 3. Position in Asset Taxonomy

```text
Knowledge Module
   └── Knowledge Assets
          └── Rule Database   ← specified here
```

The Rule Database is one Knowledge Asset, not the Knowledge Module itself.

---

# 4. Rule Definition Contract

Every rule shall define:

| Field | Requirement |
|-------|-------------|
| rule_id | Stable unique identifier within the module |
| version | Aligned to module version policy |
| category | Declared category from module taxonomy |
| status | Draft / Validated / Published / Deprecated |
| priority | Deterministic priority value or class |
| conditions | Machine-evaluable matching conditions |
| effects | Deterministic outcomes / contributions |
| evidence_schema | Required explainability fields |
| effective dating | Optional validity window |
| references | Optional upstream terminology / table references |

---

# 5. Related Rule-Oriented Assets

| Asset | Role |
|-------|------|
| Decision Tables | Compact conditional outcomes |
| Mapping Tables | Deterministic symbol/value mappings |
| Priority Tables | Ordering and conflict resolution data |
| Formula Library | Declarative coefficients and formulas |
| Reference Tables | Lookup values used by rule conditions/effects |

These assets must remain consistent with the Rule Database where co-declared.

---

# 6. Category Model

Each Rule-publishing module shall declare its category taxonomy.

Categories shall be:

- explicit
- non-overlapping in ownership
- indexed in the Manifest
- semantically stable within Version 1.x

---

# 7. Priority and Conflict Model

When multiple rules match:

1. Apply Priority Tables / priority fields.
2. Apply conflict-resolution rules if present.
3. Preserve deterministic ordering.
4. Record resolution evidence.

Runtime Engines execute priority mechanics.

Knowledge Modules supply priority data.

---

# 8. Effect Model

Rule effects may include:

- score contributions
- candidate generation or rejection
- classification assignment
- adjustment indicators
- confidence inputs

Effects shall be declarative.

Effects shall not embed imperative engine code.

---

# 9. Explainability

Every published rule shall support Evidence generation containing:

- module_id
- rule_id
- version
- category
- matched condition summary
- effect summary

---

# 10. Prohibited Content

Rules shall never contain:

- engine source code
- repository paths
- UI markup as business logic
- duplicated terminology definitions owned elsewhere
- report layout definitions

---

# 11. Acceptance Criteria

Rule assets are accepted when:

- schema-conformant;
- uniquely identified;
- category-valid;
- priority-consistent;
- explainability-complete;
- indexed and manifested;
- validated against examples and golden datasets.
