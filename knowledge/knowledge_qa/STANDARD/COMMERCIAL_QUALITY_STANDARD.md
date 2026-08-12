# Commercial Quality Standard — V1.0

| Field | Value |
|-------|-------|
| Document | COMMERCIAL_QUALITY_STANDARD |
| Standard | Knowledge QA V1.0 |

---

# 1. Purpose

Knowledge must be **consultant-grade** for paying customers.

---

# 2. Frozen tests

| Test | Pass condition |
|------|----------------|
| Paying customer | Customer benefits from hearing this once, in context |
| Consultant voice | A professional consultant would say this aloud |
| Not textbook | No dictionary definition of class or term |
| Not engine dump | No rule ids, scores, thresholds, algorithm steps |
| Not marketing | No hype, guaranteed outcomes, moral ranking |

---

# 3. Evaluation rules

1. Read claim aloud as if in a paid session.
2. Ask: “Would I charge for this sentence alone?”
3. Check banned patterns (Interpretation Standard + pack banned lists).
4. Check Customer Mode flag matches commercial use.

---

# 4. Scoring

| Score | Meaning |
|-------|---------|
| 10 | Native consultant phrasing |
| 7 | Usable with light polish |
| 5 | Textbook or generic |
| 3 | Engine or validation leak |
| 0 | Unacceptable for Customer Mode |

---

# 5. Typical failures

- “Strong means the Day Master is strong.”
- “Score above 60 indicates…”
- “Weak people should not lead.”
- “You will marry at age 32.”
- Meta-instruction: “Sell capacity, not score.”

---

# 6. Governance units

Units with `customer_mode: FORBIDDEN` or Validation-only:

- Commercial Quality may be **N/A** for Customer narrative
- Still scored for Validation/Teaching contexts if printed there

---

END
