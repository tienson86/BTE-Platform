# Claim Traceability

| Field | Value |
|-------|-------|
| Document | CLAIM_TRACEABILITY |
| Version | 1.0.0 |

---

# 1. Chain

```text
Customer Claim
      ↓
Knowledge ID
      ↓
Reasoning Decision (reason_code)
      ↓
Facts
      ↓
Evidence
```

---

# 2. ClaimTrace schema

```text
ClaimTrace
├── claim_id
├── customer_section
├── knowledge_ids[]
├── reason_codes[]
├── fact_ids[]
├── evidence_ids[]
├── gate_state
├── relevance_ref
├── salience_ref
├── language_strength
└── mode                    customer | validation
```

Every Customer Mode sentence the composer emits must map to one or more `ClaimTrace` rows.

If it cannot, the sentence is illegal.

---

# 3. Visibility

ClaimTrace is Validation Mode / diagnostics.

Customer Mode never includes ids, scores, or reason codes.

---

END
