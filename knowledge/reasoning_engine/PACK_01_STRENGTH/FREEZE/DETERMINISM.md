# Determinism — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | DETERMINISM |
| Status | FROZEN |

---

# 1. Law

Same published facts + catalog version + freeze version + context → same NarrativePlan.

No randomness.

No LLM.

No “pick the nicer sentence” inside reasoning.

---

# 2. Frozen pipeline order

```text
1. Gate (evidence policy)
2. Relevance level
3. Duplicate cluster reduction
4. Conflict actions
5. Salience level
6. Budget compression
7. Section order (below)
8. Transition intents
9. Executive summary slots from kept nodes only
```

---

# 3. Frozen sort key (lists)

Ascending:

1. `salience_level` (SAL_0 first)
2. `relevance_level` (REL_1 before REL_4)
3. `specificity` order: cause_specific, class_level, generic
4. `customer_value` order: critical, high, medium, low
5. `knowledge_id` lexicographic

---

# 4. Frozen section order (Customer Mode)

```text
Conclusion
Why
Meaning
Advantages
Challenges
Career
Marriage
Health
Luck (shell or content)
Recommendations
Executive Summary
```

Omitted domains are skipped, not reordered.

---

# 5. Duplicate / conflict / compression

Exactly as Duplicate Policy, Conflict Policy, Narrative Budget.

No extra heuristics.

---

# 6. Transitions

Reasoning emits **intent enums** only, in section order.

Composer later maps intent → wording. Wording is not this freeze’s runtime.

---

END
