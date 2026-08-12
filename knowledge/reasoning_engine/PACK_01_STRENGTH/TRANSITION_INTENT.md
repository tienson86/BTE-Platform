# Transition Intent

| Field | Value |
|-------|-------|
| Document | TRANSITION_INTENT |
| Version | 1.0.0 |

---

# 1. Split

| Layer | Job |
|-------|-----|
| Reasoning Engine | `transition_requirement` = **intent** |
| Sentence Composer | render wording |

Reasoning must not store final “Điều này đứng vững vì…” as the plan’s meaning. It stores the intent enum.

---

# 2. Intent catalog

```text
NONE
NAME_TO_CAUSE
CAUSE_TO_IMPLICATION
IMPLICATION_TO_CAPACITY
CAPACITY_TO_COST
COST_TO_DOMAIN
DOMAIN_TO_DOMAIN
DOMAIN_TO_LUCK
LUCK_INSUFFICIENT
IMPLICATION_TO_ACTION
ACTION_TO_SUMMARY
```

---

# 3. Coherence

If `RECOMMENDATION` section has no `IMPLICATION_TO_ACTION` because no implication survived, the section is not emitted (`REJECTED_NO_CHAIN`).

`WHY` must have `NAME_TO_CAUSE` from Conclusion.

---

END
