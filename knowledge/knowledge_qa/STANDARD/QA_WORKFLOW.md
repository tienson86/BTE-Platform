# QA Workflow — V1.0

| Field | Value |
|-------|-------|
| Document | QA_WORKFLOW |
| Standard | Knowledge QA V1.0 |

---

# 1. End-to-end workflow

```text
Interpretation Knowledge (authored)
  ↓
Knowledge Catalog (Draft units)
  ↓
Author self-check (QA_CHECKLIST)
  ↓
Topic phase QA (QA_TEMPLATE)
  ↓
PASS / REVIEW / FAIL
  ↓
Domain Reviewer → Reviewed
  ↓
Pack validation (QA_CHECKLIST)
  ↓
Validated
  ↓
Governance freeze
  ↓
Frozen → Reasoning consumption
```

---

# 2. When QA runs

| Trigger | Scope |
|---------|-------|
| New pack catalog | All topics, phased |
| New topic in existing pack | That topic only |
| Unit edit after Reviewed | That unit |
| Golden / Reasoning policy change | Affected units only |
| Pre-freeze gate | All Validated units in pack |

---

# 3. Topic phase order (recommended)

For Strength-style packs:

```text
MEANING → CAUSES → ADVANTAGES → CHALLENGES → PERSONALITY
  → CAREER → WEALTH → MARRIAGE → HEALTH → LUCK
  → RECOMMENDATION → EDGE_CASES → EXAMPLES
```

Order may vary by pack; **MEANING before ADVANTAGES** is mandatory when advantages restate identity.

---

# 4. QA task boundaries

### QA-only task (review)

- Score criteria
- Assign verdict
- Document gaps
- **Do not** rewrite claims
- **Do not** change catalog status
- **Do not** edit schema or clusters

### Authoring task (fix)

- Edit claim, limitations, metadata
- Re-submit for re-QA

---

# 5. Outputs per phase

Each phase produces one review file:

```text
knowledge/knowledge_qa/PACK_XX_<DOMAIN>/PHASE_NN_<TOPIC>_REVIEW.md
```

Required sections: see [QA_TEMPLATE.md](QA_TEMPLATE.md).

---

# 6. Scale (thousands of units)

| Practice | Rule |
|----------|------|
| Batch size | One topic phase at a time |
| Automation | QA Assistant scores; human approves |
| Storage | Markdown reviews V1.0; indexed store future |
| Regression | Re-QA affected ids on policy change |
| Sampling | Full QA required before Validated; spot audit after Frozen |

---

END
