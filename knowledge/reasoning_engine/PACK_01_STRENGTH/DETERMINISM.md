# Determinism

| Field | Value |
|-------|-------|
| Document | DETERMINISM |
| Version | 1.0.0 |

---

# 1. Rule

Same:

```text
facts + knowledge_version + reasoning_policy_version + context
```

→ same `NarrativePlan`.

---

# 2. Forbidden sources of drift

- random
- LLM
- hash-set iteration without sort
- wall-clock
- “pick the more beautiful sentence”

---

# 3. Ordering

All lists sorted by:

1. narrative_priority
2. purpose enum order
3. salience desc
4. knowledge_id asc (tie-break)

---

# 4. Test

Run twice on CASE-0001 fixture. Canonical JSON of NarrativePlan must match.

---

END
