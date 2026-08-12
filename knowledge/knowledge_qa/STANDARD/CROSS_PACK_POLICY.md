# Cross-Pack Policy — V1.0

| Field | Value |
|-------|-------|
| Document | CROSS_PACK_POLICY |
| Standard | Knowledge QA V1.0 |

---

# 1. Purpose

Knowledge units must be **selectable in isolation** within their owning pack unless a cross-pack dependency is explicitly declared and satisfied.

---

# 2. Frozen terms

| Term | Definition |
|------|------------|
| **Required Packs** | Packs whose published facts are available for the case at runtime |
| **Cross-Pack Dependency** | Unit true only if another pack’s facts or doctrine are present |
| **Pack isolation** | Unit evaluable with owning pack facts only |
| **Safe omission** | If dependency pack absent, unit rejected — never guessed |
| **Future activation** | Dependency documented; inactive until pack published |

---

# 3. Rules

| Rule | QA consequence |
|------|----------------|
| Strength unit requires Pattern fact | FAIL Cross-Pack unless Pattern published |
| Soft career example (“leader role”) | REVIEW if no hard dependency |
| Luck decade guarantee without luck pack | FAIL Evidence + Cross-Pack |
| Useful God named without UG pack | FAIL Cross-Pack |
| Marriage advice requiring spouse chart | Cross-pack — declare or FAIL |

---

# 4. Scoring (Cross-Pack Dependency criterion)

| Score | Condition |
|-------|-----------|
| 10 | Fully isolated |
| 8 | Soft example bleed only |
| 5 | Implied other pack; still printable without it |
| 3 | Requires unpublished pack for truth of claim |
| 0 | Hard dependency; will misfire in Strength-only mode |

---

# 5. Declaration format

When dependency exists and is intentional:

- Document in unit `limitations`
- Register in pack governance cross-pack registry (future tooling)
- Set `required_facts` to include foreign pack keys **only when published**

Until registry exists, limitations text + governance record suffice.

---

# 6. PACK-01 Strength default

PACK-01 Strength units default to **pack isolation**.

Luck units use `luck_interaction` only when Luck Engine publishes interaction state — not invented polarity.

---

END
