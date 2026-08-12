# Conflict Policy — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | CONFLICT_POLICY |
| Status | FROZEN |

---

# 1. Categories (frozen)

| Code | Meaning |
|------|---------|
| `FACT` | Two published facts disagree in polarity (CASE-0001 C1) |
| `KNOWLEDGE` | Two catalog claims cannot both be true as stated |
| `DOMAIN` | Two domains imply opposite life policies without a condition |
| `ADVICE` | Do vs do / do vs avoid without a condition |
| `CONFIDENCE` | Unit requires a higher confidence band than input |

---

# 2. Resolution actions (frozen)

| Action | Code | Effect |
|--------|------|--------|
| Qualify | `CONFLICT_QUALIFY` | Keep both with condition; Customer Mode **must** bind them in one weather |
| Defer | `CONFLICT_DEFER` | Validation only; Customer insufficient or omit |
| Expose | `CONFLICT_EXPOSE_VALIDATION` | Validation conflict record; **not** two unexplained Customer headlines |
| Drop one | `REJECTED_CONFLICT` | Only if catalog `conflicts` says they are mutually exclusive **and** not nuance |

---

# 3. Qualification (C1)

Support-side strengthen **and** control weaken:

- Action: `CONFLICT_QUALIFY`
- Why keeps **both** polarities
- Class does **not** flip
- Conclusion `language_strength = qualified`

This is **conditional nuance**, not a true contradiction.

---

# 4. When Customer Mode must never see both claims

If `KNOWLEDGE` or `ADVICE` is a **true contradiction** (no catalog condition):

- Do not emit both as separate Customer assertions
- Either qualify with an explicit `when`, or drop one (`REJECTED_CONFLICT`), and always `CONFLICT_EXPOSE_VALIDATION`

Example forbidden: “You are decisive.” and “You hesitate under pressure.” as two unexplained headlines.

Allowed: one qualified node that names the condition (control present).

---

# 5. Alternative class

Runner-up class → Validation (`DEFERRED_TO_VALIDATION`).

Customer Mode: not a second conclusion.

`REJECTED_ALTERNATIVE_CLASS_AS_PRIMARY` for MEAN-BA on a Strong case.

---

# 6. Advice safety

Absolute career/investment commands from Strength alone → `REJECTED_ADVICE_UNSAFE`.

---

END
