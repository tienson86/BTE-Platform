# Alternative Reasoning

| Field | Value |
|-------|-------|
| Document | ALTERNATIVE_REASONING |
| Version | 1.0.0 |

---

# 1. Default

```text
Alternative Analysis → Validation Mode
```

Customer Mode does not print `Strong 72% / Balanced 28%`.

---

# 2. Decisions the engine must make

Given primary Strong and runner-up Balanced:

1. Primary conclusion remains Strong (published class).
2. Claims that are **only true of Very Strong / deep surplus** are ineligible (`root_thin`, not extreme).
3. Claims that are **borderline-sensitive** (generic “unbreakable”, “never hesitate”) are dropped or qualified.
4. Language_strength on Conclusion = `qualified` if runner-up is material.
5. Customer may get **one** EDGE_QUALIFIER (“not extreme surplus / still checked by pressure”), not a second class.

---

# 3. When alternative is omitted from Validation

Only if `none_plausible` was already computed upstream and no C1 / thin-root / boundary.

If upstream provided a runner-up, Reasoning Engine **keeps** it in Validation diagnostics.

---

# 4. What not to do

- Flip class to Balanced to please an expert label (not in input).
- Average two classes.
- Load Balanced MEANING units into Customer Mode.
- Show shares to the customer.

---

END
