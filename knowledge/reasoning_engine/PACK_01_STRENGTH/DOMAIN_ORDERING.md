# Domain Ordering

| Field | Value |
|-------|-------|
| Document | DOMAIN_ORDERING |
| Version | 1.0.0 |

---

# 1. Default narrative order (PACK-01)

This is a **default narrative order**, not a BaZi law.

```text
1. Core Strength (conclusion, why, meaning, advantages, challenges)
2. Personality
3. Decision Making
4. Career
5. Wealth
6. Marriage
7. Health
8. Learning / Leadership (if kept)
9. Luck
10. Recommendations
11. Executive Summary
```

PACK-01 must **not** infer that Career is always more important than Marriage in life. The list is only a stable default for determinism.

---

# 2. question_context (future)

```text
context.question_context = wealth | career | marriage | health | luck | general
```

Effects (design):

| Context | Up | Down / omit |
|---------|----|-------------|
| `wealth` | Wealth, related recs | Marriage may omit |
| `career` | Career, leadership, decision | Health may compress |
| `marriage` | Marriage, personality | Career secondary |
| `general` | default | — |

PACK-01 need not implement runtime context. Architecture must accept the field.

Omitted domains go to `omitted_domains[]` with `REJECTED_DOMAIN_NOT_REQUESTED`.

---

# 3. Coherence dependencies

```text
WHY           requires CONCLUSION
MEANING       requires WHY or explicit insufficient why
ADVANTAGE     requires MEANING or CONCLUSION
CHALLENGE     requires MEANING or CONCLUSION
DOMAIN        requires at least CONCLUSION
RECOMMENDATION requires at least one IMPLICATION in chain
SUMMARY       requires CONCLUSION + at least one other kept section
LUCK          may be insufficient shell without other luck units
```

A section with no logical predecessor is not emitted (except Conclusion).

---

END
