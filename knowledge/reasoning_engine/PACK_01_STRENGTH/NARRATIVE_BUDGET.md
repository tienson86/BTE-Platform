# Narrative Budget

| Field | Value |
|-------|-------|
| Document | NARRATIVE_BUDGET |
| Version | 1.0.0 |

---

# 1. Principle

> More knowledge is not a better interpretation.

The Reasoning Engine must not pass every eligible unit to the composer.

---

# 2. PACK-01 default budget (units kept for Customer Mode)

| Slot | Min | Max | Notes |
|------|-----|-----|-------|
| Core conclusion | 1 | 1 | From classification, not a pile of units |
| Why | 2 | 4 | Present causes only; C1 should keep both polarities if both present |
| Meaning | 1 | 2 | |
| Advantages | 2 | 4 | |
| Challenges | 2 | 4 | |
| Personality | 0 | 2 | omit if budget/question_context says so |
| Career | 0 | 3 | |
| Wealth | 0 | 3 | |
| Marriage | 0 | 3 | |
| Health | 0 | 3 | |
| Learning / Leadership / Decision | 0 | 1 each | secondary unless salient |
| Luck | 0 | 3 | 0 content units if MISSING — shell only |
| Recommendations | 2 | 5 | must chain from kept implications |
| Warnings | 0 | 2 | |
| Edge qualifier | 0 | 1 | |
| Executive Summary claims | 5 | 8 | not extra knowledge; compression |

`verbosity = short` uses the mins (and may omit optional domains).

`question_context = wealth` may set Wealth max 3 and Marriage max 0.

---

# 3. Cut order when over budget

1. generic specificity
2. lowest salience
3. duplicates already clustered
4. supporting-only (relevant, not salient)
5. domains not in question_context
6. never cut Conclusion
7. never cut the last Why if it is the only causal polarity of C1 (both sides of a live conflict should remain if they fit Why max 4)

---

# 4. Under budget

Do not fill with generic units.

See [NARRATIVE_EXPANSION.md](NARRATIVE_EXPANSION.md).

---

# 5. Validation Mode

Validation Mode has **no customer budget**. It lists candidates, rejected, ranks.

Customer Mode is budgeted.

---

END
