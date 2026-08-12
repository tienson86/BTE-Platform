# Claim Trace — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | CLAIM_TRACE |
| Status | FROZEN |

---

# 1. Chain (frozen)

Every Customer Mode sentence the composer later emits must map to:

```text
Sentence
  → knowledge_id(s)
    → primary reason_code
      → evidence_id(s)
        → fact key(s)
```

If a sentence cannot map, it is illegal. Do not emit it.

---

# 2. ClaimTrace record

```text
claim_id
section
knowledge_ids[]
reason_code
evidence_ids[]
fact_keys[]
gate_state
relevance_level
salience_level
language_strength
mode
```

Mode A / Validation stores the full record.

Customer Mode stores none of the ids, codes, or levels.

---

# 3. Future audit

A reviewer must answer “why is this paragraph here?” by opening the trace, not by asking a model.

Regression: golden CASE-0001 traces must match this freeze.

Composer tests: no sentence without a trace row.

---

END
