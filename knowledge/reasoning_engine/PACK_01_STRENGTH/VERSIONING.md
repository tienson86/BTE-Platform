# Versioning

| Field | Value |
|-------|-------|
| Document | VERSIONING |
| Version | 1.0.0 |

---

# 1. Fields on every NarrativePlan

```text
reasoning_schema_version      structure of ReasoningInput / NarrativePlan
reasoning_policy_version      weights, budget numbers, language mapping
knowledge_version             interpretation knowledge pack
standard_version              interpretation standard pack
```

PACK-01 design: all `1.0.0` at this writing.

---

# 2. Compatibility

Schema bump if fields are removed or change meaning.

Policy bump if budget/salience tables change (same schema).

Knowledge bump independent — plan must record which knowledge it reasoned over.

---

# 3. Trace

Reviewer must know which four versions produced a CASE-0001 plan.

---

END
