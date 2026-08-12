# Traceability Standard — V1.0

| Field | Value |
|-------|-------|
| Document | TRACEABILITY_STANDARD |
| Standard | Knowledge QA V1.0 |

---

# 1. Purpose

Enable audit from customer-facing claim back to source and engine facts.

---

# 2. Frozen audit chain

```text
Knowledge Unit (knowledge_id)
  ↓
Claim (one So what)
  ↓
Reason (reason_codes — assigned at Reasoning selection)
  ↓
Evidence (published fact keys + states)
  ↓
Fact (Engine output)
```

Knowledge QA validates **Knowledge → Claim → Source → Evidence declaration**.

Reason layer validates **Reason → Evidence → Fact** at runtime.

---

# 3. Required metadata

| Field | Rule |
|-------|------|
| `knowledge_id` | Stable; never reused after Deprecated |
| `source_document` | Exact Interpretation Knowledge filename |
| `required_facts` | Every fact claim depends on |
| `limitations` | Gates when facts absent |
| `duplicate_cluster` | If member, traceable to governance id |

---

# 4. Evaluation

| Check | FAIL if |
|-------|---------|
| Source exists | File missing or wrong path |
| Claim in source | Paraphrase untraceable to paragraph |
| Composite claim | Multiple sources without split units |
| Orphan unit | No source_document |

---

# 5. Scoring

| Score | Condition |
|-------|-----------|
| 10 | Full chain documented |
| 7 | Source ok; fact chain in limitations only |
| 5 | Vague source reference |
| 3 | Untraceable paraphrase |
| 0 | No source |

---

# 6. QA record traceability

Phase reviews must list:

- Unit id
- Source file
- Verdict
- Blocking criteria

Template: [QA_TEMPLATE.md](QA_TEMPLATE.md).

---

END
